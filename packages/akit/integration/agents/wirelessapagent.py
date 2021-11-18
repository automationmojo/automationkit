
from typing import Any, Optional, Sequence, Tuple, Union

import json
import os
import re
import time
import traceback

from akit.exceptions import AKitConfigurationError, AKitOpenWRTRequestError

from akit.integration.agents.sshagent import SshAgent, SshSession
from akit.integration.wireless.constants import (
    DeAuthenticationReason, MfpMode, OpenWrtModel, WirelessEncryption,
    DEFAULT_REGION_CODE, REGION_CODES)
from akit.integration.wireless.channels import G_CHANNEL_MAPPING, N_CHANNEL_MAPPING, WifiChannelInfo

from akit.integration.wireless.fastpingresult import FastPingResult
from akit.integration.wireless.stationinfo import StationInfo

from akit.aspects import Aspects, DEFAULT_ASPECTS
from akit.integration.credentials.sshcredential import SshCredential

from  akit.xlogging.foundations import getAutomatonKitLogger

class WirelessApAgent:
    """
        The :class:`WirelessApAgent` provides an implementation of a administrative
        interface for devices that are running the OpenWRT wireless router software.
    """

    logger = getAutomatonKitLogger()

    SET_OF_WIFI_RESTART_ERRORS_TERMS = set(('error', 'invalid'))

    def __init__(self, ap_host: str, admin_credential: SshCredential, port: int=22, aspects: Aspects=DEFAULT_ASPECTS):
        self._ap_host: str = ap_host
        self._admin_credential: SshCredential = admin_credential
        self._port: int = port
        self._aspects: Aspects = aspects

        self._ssh_agent: SshAgent = SshAgent(self._ap_host, self._admin_credential, aspects=aspects)
        self._ssh_session: SshSession = None

        self._model_name: str = None
        self._openwrt_version: str = None
        return

    def arping_bcast(self, interface: str, count: int, host: str) -> int:
        """
            Send specified count of broadcast arping requests out specified interface

            :param interface: interface requests to egress
            :param count: number of ICMP requests
            :param host: host to broadcast arp requests for

            :returns: integer replies
        """
        replies = 0
        
        command = 'arping -b -I {} -c {} {}'.format(interface, count, host)
        
        status, stdout, stderr = self._ssh_run_command(command)
        if status == 0:
            ping_lines = stdout.splitlines()

            if len(ping_lines) > 0:
                rcvd_lines = [line for line in ping_lines if 'Received' in line]
                if len(rcvd_lines) > 0:
                    line_parts = rcvd_lines[0].split(' ')
                    replies = int(line_parts[1])

                    self.logger.debug("Parsed arping broadcast replies as <{}>".format(replies))

        return replies

    def commit_wifi_config(self):
        """
            Commits the current wireless configuration to the save file
        """
        command = 'uci commit wireless'

        status, stdout, stderr = self._ssh_run_command(command)
        if status != 0:
            errmsg ="Error while committing wireless configuration changes to file."
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return

    def commit_wifi_config_and_restart_wifi(self):
        """
            Commits the current wifi configuration settings and restarts the wifi radio's.
        """
        self.commit_wifi_config()
        self.restart_wifi()
        return

    def configured_channel_is_dfs(self, dev: int) -> bool:
        """
            Returns True if current channel is a DFS channel.

            .. note::
                CAC is complete when logread reports "DFS-CAC-COMPLETED", which
                takes roughly 60 seconds.

            :param dev: the index of wifi device to test

            :returns: whether or not current channel is a DFS channel

        """
        rtnval = False

        curr_chan = self.get_channel(dev)
        for chanmap in N_CHANNEL_MAPPING[4:-5]:
            if curr_chan == chanmap.channel:
                rtnval = True
                break

        return rtnval

    def del_client(self,
                   dev: int,
                   client_mac: str,
                   reason: DeAuthenticationReason=DeAuthenticationReason.PREV_AUTH_NOT_VALID,
                   bantime_ms: int=0):
        """
            Tells the openWRT AP to deauthenticate the client_mac device.

            :param dev: network interface
            :param client_mac: mac address of client, including colons.
            :param reason: Deauth reason code
            :param bantime_ms: Prevent client from reconnecting for bantime_ms milliseconds
        """
        del_client_args = {
            "addr": client_mac,
            "reason": reason,
            "deauth": True,
            "ban_time": bantime_ms
        }

        command = "ubus call hostapd.wlan{} del_client '{}'".format(dev, json.dumps(del_client_args))
        
        status, stdout, stderr = self._ssh_run_command(command)
        if status != 0:
            errmsg ="Error trying to deauthenticate dev={} mac={}".format(dev, client_mac)
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return

    def delete_basic_rate(self, dev: int):
        """
            Deletes the supported basic rates setting. Each basic_rate is measured in kb/s.
            This option only has an effect on ap and adhoc wifi-ifaces.
            
            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'basic_rate')
        return

    def delete_beacon_int(self, dev: int):
        """
            Deletes the beacon interval

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'beacon_int')
        return

    def delete_channel(self, dev: int):
        """
            Deletes that channel setting for the specified device.

            :param dev: the wifi device to set the channel on
            
            :raises ValueError: if the channel provided is unsupported for the wireless device
        """
        self.delete_radio(dev, 'channel')
        return

    def delete_disabled(self, dev: int):
        """
            Delete the setting to enable or disable the radio.

            :param dev: the radio (0 or 1)

            ..note: AP default = 1

        """
        self.delete_radio(dev, 'disabled')
        return

    def delete_diversity(self, dev: int):
        """
            Enables or disables the automatic antenna selection by the driver.
            Note: AP default = 1

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'diversity')
        return

    def delete_dtim_period(self, dev: int):
        """
            Clears the DTIM (delivery traffic information message) period.

            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'dtim_period')
        return

    def delete_encryption(self, dev: int):
        """
            Delete the wireless encryption setting

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'encryption')
        return

    def delete_fragmentation_threshold(self, dev: int):
        """
            Sets the WiFi frame fragmentation threshold for a given radio

            :param dev: the radio (0 or 1)
        """
        self.delete_radio(dev, 'frag')
        return

    def delete_hidden(self, dev: int):
        """
            Delete the setting for SSID broadcasting if set to 1

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'hidden')
        return

    def delete_hwmode(self, dev: int):
        """
            Selects the wireless protocol to use, possible values are 11b, 11bg, 11g,
            11gdt (G + dynamic turbo, madwifi only), 11gst (G turbo, broadcom only), 11a,
            11adt (A + dynamic turbo, madwifi only), 11ast (A + static turbo, madwifi only),
            11fh (frequency hopping), 11lrs (LRS mode, broadcom only), 11ng (11N+11G, 2.4GHz,
            mac80211 only), 11na (11N+11A, 5GHz, mac80211 only) or auto.
            
            ..note: AP default =  driver default

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'hwmode')
        return

    def delete_htmode(self, dev: int):
        """
            Deletes the channel width in 11ng and 11na mode, possible values are: HT20
            (single 20MHz channel), HT40- (2x 20MHz channels, primary/control channel is upper,
            secondary channel is below) or HT40+ (2x 20MHz channels, primary/control channel is
            lower, secondary channel is above. This option is only used for type mac80211.

            ..note: mac80211 is the default, we never change this.
                    AP default =  driver default

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'htmode')
        return

    def delete_ht_capab(self, dev):
        """
            Specifies the available capabilities of the radio. The values are autodetected.
            This option is only used for type mac80211.
            
            ..note: mac80211 is the default, we never change this.
                    AP default =  driver default
            
            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'ht_capab')
        return


    def delete_ieee80211w(self, dev:int):
        """
            Clears the management frame protection (802.11w) value

            ..note:: AP should be set for some wpa-psk encryptiopn setting in order for
                     ieee80211w to be set to some non-zero value.

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'ieee80211w')
        return

    def delete_isolate(self, dev: int):
        """
            Isolate wireless clients from each other, only applicable in ap mode.
            Note: May not be supported in the original Backfire release for mac80211.

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'isolate')
        return

    def delete_key(self, dev: int, key_ordinal: Optional[int]=None):
        """
            Get key parameter. In wep mode, returns index, wpa mode, returns passphrase

            :param dev: the wifi device index to set the region on
            :param key_ordinal: the ordinal to append to the key name
        """
        key_name = 'key'
        if key_ordinal is not None:
            key_name += str(key_ordinal)

        self.delete_wifi_iface(dev, key_name)
        return


    def delete_log_level(self, dev: int):
        """
            Delete the log_level setting. Supported levels are:
                0 = verbose debugging
                1 = debugging,
                2 = informational messages
                3 = notification
                4 = warning

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'log_level')
        return

    def delete_macaddr(self, dev: int):
        """
            Deletes the override MAC address used for the wifi interface.

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'macaddr')
        return

    def delete_macfilter(self, dev: int):
        """
            Deletes the specified the mac filter policy, disable to disable the filter, allow to
            treat it as whitelist or deny to treat it as blacklist.

            ..note: Supported for the mac80211 since r25105
                    AP default = disable

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'macfilter')
        return

    def delete_maclist(self, dev: int):
        """
            Deletes the list of MAC addresses to put into the mac filter.

            ..note: Supported for the mac80211 since r25105

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'maclist')
        return


    def delete_max_listen_int(self, dev: int):
        """
            Clears the maximum allowed STA (client) listen interval. Association will be
            refused if a STA attempts to associate with a listen interval greater than
            this value. This option only has an effect on ap wifi-ifaces.

            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'max_listen_int')
        return

    def delete_maxassoc(self, dev: int):
        """
            Deletes the specified maximum number of clients to connect.

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'maxassoc')
        return

    def delete_mcast_rate(self, dev: int):
        """
            Clears the fixed multicast rate, measured in kb/s.
            
            ..note: Only supported by madwifi, and mac80211 (for type adhoc)

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'mcast_rate')
        return

    def delete_mode(self, dev: int):
        """
            Deletes the selecttion for the operation mode of the wireless network, ap for
            Access Point, sta for managed (client) mode, adhoc for Ad-Hoc, wds for static
            WDS and monitor for monitor mode, mesh for 802.11s mesh mode.

            ..note: mesh mode only supported by mac80211

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'mode')
        return

    def delete_network(self, dev: int):
        """
            Specifies the network interface to attach the wireless to.
            lan, wan, etc.

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'network')
        return

    def delete_noscan(self, dev:int):
        """
            Delete the do not scan for overlapping BSSs in HT40+/- mode.
            
            ..note: Only supported by mac80211 Turning this on will
                violate regulatory requirements!

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'noscan')
        return

    def delete_radio(self, dev: int, parameter: str):
        """
            delete radio configuration option on OpenWrt AP.
            If no value is passed for a given param then the option is deleted.

            :param dev: device (0 or 1)
            :param parameter: parameter being configured
        """
        prop_name = 'wireless.radio{}.{}'.format(dev, parameter)
        self.uci_delete(prop_name)
        return

    def delete_region(self, dev: int, country_code: str):
        """
        Delete the wireless region configuration setting.

        :param dev: the wifi device index to set the region on
        
        .. note::
            Region code modifications shall only be made on APs located in
            isolation chambers or screen rooms.

        """
        if country_code not in REGION_CODES:
            raise ValueError("Invalid country code: {}".format(country_code))

        return self.delete_radio(dev, 'country')

    def delete_rxantenna(self, dev: int):
        """
            Specifies the antenna for receiving, the value may be driver specific,
            usually it is 1 for the first and 2 for the second antenna. Specifying 0
            enables automatic selection by the driver if supported. This option has
            no effect if diversity is enabled.

            ..note: AP default = Driver default

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'rxantenna')
        return

    def delete_ssid(self, dev: int):
        """
            Delete the broadcasted SSID of the wireless network (for managed mode the SSID of the network
            you're connecting to).

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'ssid')
        return

    def delete_txantenna(self, dev: int):
        """
            Removes the specified antenna for transmitting, values are identical to rxantenna.
            ..note: AP default = Driver default

            :param dev: the wifi device index to set the region on
        """
        self.delete_radio(dev, 'txantenna')
        return

    def delete_txpower(self, dev: int):
        """
            Delete the specified the transmission power in dB.
            
            ..note: AP default =  driver default

            :param dev: the wifi device index to set the region on
        """
        return self.delete_radio(dev, 'txpower')

    def delete_wep_rekey(self, dev: int):
        """
            Deletes the specified rekey interval in seconds.

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'wep_rekey')
        return

    def delete_wifi_iface(self, dev, param):
        """
        Delete wireless interface configuration setting on OpenWrt AP
        
        :param dev: device (0 or 1)
        :param parameter: parameter being configured
        """
        prop_name = 'wireless.@wifi-iface[{}].{}'.format(dev, param)
        self.uci_delete(prop_name)
        return

    def delete_wmm(self, dev: int):
        """
            Clears the wmm setting on the device interface

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'wmm')
        return

    def delete_wpa_group_rekey(self, dev: int):
        """
            Deletes the specified the rekey interval in seconds

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'wpa_group_rekey')
        return

    def delete_wpa_pair_rekey(self, dev: int):
        """
            Delete the specified rekey interval in seconds

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'wpa_pair_rekey')
        return

    def deletes_wps_device_name(self, dev: int):
        """
            Gets the wps_devicename string

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'wps_device_name')
        return

    def delete_wps_manufacturer(self, dev: int):
        """
            Clears the wps_manufacturer string

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'wps_manufacturer')
        return

    def delete_wps_pushbutton(self, dev: int):
        """
            Clears the wps_pushbutton config to be either 1 or 0

            :param dev: the wifi device index to set the region on
        """
        self.delete_wifi_iface(dev, 'wps_pushbutton')
        return

    def fping(self, host: str, count: int, delay: int) -> FastPingResult:
        """
            fping device from OpenWrt AP. fping is not istalled by default on image
            and needs to be installed with opkg. Available in packages folder on
            openWrt website.

            :param host: device to ping (ip or hostname)
            :param count: number of ICMP requests
            :param delay: interval between ping packets to one target (in ms)

            :returns: summary results from the fping command
        """
        command = 'fping -q -c {} -p {} {}'.format(count, delay, host)

        status, stdout, stderr = self._ssh_run_command(command)
        if status != 0:
            errmsg ="Expected fping results but got"
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        ping_lines = stdout.splitlines()
        rcv_line = [line for line in ping_lines if 'xmt/rcv/' in line]
        if len(rcv_line) == 0:
            raise ValueError("Expected to find 'xmt/rcv/%loss' line but got {}".format(stdout))

        summary_data = rcv_line[0].split(' ')[4].split('/')
        result = map(int, summary_data[:-1])
        result.append(float(summary_data[-1].strip(' %,')) * .01)

        result = FastPingResult(*result)

        self.logger.debug('Parsed fping result as {}'.format(result))

        return result

    def get_2ghz_mac_address(self):
        """
            Gets MAC address of the 2ghz radio
        """
        rtnval = None

        command = 'ifconfig wlan{}'.format(self.radio_iface_idx_2ghz)
        status, stdout, stderr = self._ssh_run_command(command)
        m = re.search('HWaddr (.{17})', stdout)

        if m is not None:
            rtnval = m.group(1).lower()
        else:
            errmsg ="Unable to get 2GHz MAC address"
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return rtnval

    def get_2ghz_radio_index(self):
        """
            The interface index corresponding the the 2GHz radio
        """
        rtnval = None

        model_name = self.get_model_name()
        if model_name == OpenWrtModel.NETGEAR_7600.value:
            rtnval = 1
        elif model_name in (OpenWrtModel.NETGEAR_WNDR3700.value,
                            OpenWrtModel.NETGEAR_WNDR3700_1907.value):
            rtnval = 0
        else:
            errmsg ="Unsupported Model {}.".format(model_name)
            raise AKitOpenWRTRequestError(errmsg)

        return rtnval

    def get_5ghz_mac_address(self) -> str:
        """
            Gets the MAC address of the 5ghz radio
        """
        rtnval = None

        command = 'ifconfig wlan{}'.format(self.radio_iface_idx_5ghz)
        status, stdout, stderr = self._ssh_run_command(command)
        if status == 0:
            m = re.search('HWaddr (.{17})', stdout)

            if m:
                rtnval = m.group(1).lower()
            else:
                errmsg ="Unable to parse 5GHz MAC address"
                raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)
        else:
            errmsg ="Unable to get 5GHz MAC address"
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return rtnval

    def get_5ghz_radio_index(self) -> int:
        """
            Gets the interface index corresponding the the 5GHz radio
        """
        idx_2ghz = self.get_2ghz_radio_index()
        rtnval = 0 if idx_2ghz == 1 else 1
        return rtnval

    def get_basic_rate(self, dev: int):
        """
            Get the supported basic rates. Each basic_rate is measured in kb/s.
            This option only has an effect on ap and adhoc wifi-ifaces.
            
            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param basic_rate: The basic rate to set
        """
        rtnval = self.get_radio(dev, 'basic_rate')
        return rtnval

    def get_beacon_int(self, dev: int) -> str:
        """
            Gets the beacon interval

            :param dev: the wifi device index to set the region on

            :returns: beacon_int
        """
        rtnval = self.get_radio(dev, 'beacon_int')
        return rtnval

    def get_channel(self, dev: int) -> str:
        """
            Return the wireless configured channel.

            :param dev: the wifi device index to get the channel for

            :returns: the configured channel
        """
        rtnval = self.get_radio(dev, 'channel')
        return rtnval

    def get_connected_stations(self, dev: int) -> Tuple[StationInfo]:
        """
        Executes the command iw dev station dump on the AP. Output will return detailed
        info on all connected wireless client(s) to the AP.

        :param dev: network interface on AP
        
        :returns: the station dump info as a tuple of

        """
        sta_list = []

        command = 'iw wlan{} station dump'.format(dev)
        status, stdout, stderr = self._ssh_run_command(command)

        if status == 0:
            for client_dump in re.split('Station ', stdout.replace('\r', ''), re.DOTALL)[1:]:

                sta = dict(re.findall(r'\s+(.+):\s*(.+)', client_dump))
                sta['mac'], sta['wlan'] = re.search(
                    r'(..:..:..:..:..:..) \(on (.+)\)', client_dump).groups()

                for k, v in sta.items():
                    sta[k] = self._try_convert_primitive(v)

                try:
                    sta_list.append(
                        StationInfo(
                            mac=sta['mac'],
                            inactive_time=sta['inactive time'],
                            rx_bytes=sta['rx bytes'],
                            rx_packets=sta['rx packets'],
                            rx_drop_misc=sta['rx drop misc'],
                            rx_bitrate= sta.get('rx bitrate', ''),
                            tx_bytes=sta['tx bytes'],
                            tx_packets=sta['tx packets'],
                            tx_retries=sta['tx retries'],
                            tx_failed=sta['tx failed'],
                            tx_bitrate=sta['tx bitrate'],
                            signal=sta['signal'],
                            signal_avg=sta['signal avg'],
                            exp_throughput=sta.get('expected throughput', ''),
                            # sta['rx duration'],
                            # sta['last ack signal'],
                            count_authorized=sta['authorized'],
                            count_authenticated=sta['authenticated'],
                            count_associated=sta['associated'],
                            wmm=sta['WMM/WME'],
                            mfp=sta['MFP'],
                            tdls_peer=sta['TDLS peer'],
                            dtim_period=sta['DTIM period'],
                            beacon_interval=sta['beacon interval'],
                            preamble=sta['preamble'],
                            short_preamble=sta.get('short preamble',''),
                            short_slot_time=sta['short slot time'],
                            connected_time=sta['connected time']))

                except KeyError as e:
                    errmsg = traceback.format_exec()
                    raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return tuple(sta_list)

    def get_dtim_period(self, dev: int) -> int:
        """
            Gets the DTIM (delivery traffic information message) period. There will
            be one DTIM per this many beacon frames. This may be set between 1 and
            255. This option only has an effect on ap wifi-ifaces.

            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on

            :returns: the delivery traffic information message period
        """
        rtnval = self.get_wifi_iface(dev, 'dtim_period')
        return rtnval

    def get_diversity(self, dev: int) -> bool:
        """
            Gets whether diversity is enabled or disabled.
            Note: AP default = 1

            :param dev: the wifi device index to set the region on

            :returns: whether diversity is enabled or disabled
        """
        self.get_radio(dev, 'diversity')
        return

    def get_encryption(self, dev: int) -> str:
        """
            Return wireless encryption setting

            :param dev: the wifi device index to set the region on
            
            :returns: the encryption method
        """
        rtnval = self.get_wifi_iface(dev, 'encryption')
        return rtnval

    def get_fragmentation_threshold(self, dev: int) -> int:
        """
            Gets the WiFi frame fragmentation threshold for a given radio

            :param dev: the radio (0 or 1)

            :returns: the fragmentation size or None if it is not set.
        """
        rtnval = self.get_radio(dev, 'frag')
        return rtnval

    def get_hidden(self, dev: int) -> str:
        """
            Delete the setting for SSID broadcasting if set to 1

            :param dev: the wifi device index to set the region on
        """
        rtnval = self.get_wifi_iface(dev, 'hidden')
        return rtnval

    def get_hwmode(self, dev):
        """
            Return the hwmode

            :param dev: the wifi device index to set the region on

            :returns: returns the hwmode of the specified device
        """
        rtnval = self.get_radio(dev, 'hwmode')
        return rtnval

    def get_ht_capab(self, dev) -> str:
        """
            Gets the pecified the available capabilities of the radio. The values are autodetected.
            This option is only used for type mac80211.
            
            ..note: mac80211 is the default, we never change this.
                    AP default =  driver default
            
            :param dev: the wifi device index to set the region on
        """
        rtnval = self.get_radio(dev, 'ht_capab')
        return rtnval

    def get_htmode(self, dev: int, htmode: int):
        """
            Specifies the channel width in 11ng and 11na mode, possible values are: HT20
            (single 20MHz channel), HT40- (2x 20MHz channels, primary/control channel is upper,
            secondary channel is below) or HT40+ (2x 20MHz channels, primary/control channel is
            lower, secondary channel is above. This option is only used for type mac80211.

            ..note: mac80211 is the default, we never change this.
                    AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param htmode: the htmode to set
        """
        rtnval = self.get_radio(dev, 'htmode')
        return rtnval

    def get_ieee80211w(self, dev:int) -> int:
        """
            Gets the management frame protection (802.11w) value

            ..note:: AP should be set for some wpa-psk encryptiopn setting in order for
                     ieee80211w to be set to some non-zero value.

            :param dev: the wifi device index to set the region on

            :returns: value to set for 802.11w, which has the following
                      meaning for openwrt: 2=required, 1=optional,
                      0=802.11w is disabled (same as ieee80211w setting being absent)
        """
        rtnval = self.get_wifi_iface(dev, 'ieee80211w')
        return rtnval

    def get_isolate(self, dev: int) -> bool:
        """
            Isolate wireless clients from each other, only applicable in ap mode.
            Note: May not be supported in the original Backfire release for mac80211.

            :param dev: the wifi device index to set the region on
            :returns: A boolean indicating to isolate wireless clients
        """
        rtnval = self.get_wifi_iface(dev, 'isolate')
        return rtnval

    def get_key(self, dev: int, key_ordinal: Optional[int]=None) -> Union[int, str]:
        """
            Get key parameter. In wep mode, returns index, wpa mode, returns passphrase

            :param dev: the wifi device index to set the region on
            :param key_ordinal: the ordinal to append to the key name

            :returns: the key information integer key (WEP mode), string key (wpa-psk mode)
        """
        key_name = 'key'
        if key_ordinal is not None:
            key_name += str(key_ordinal)

        rtnval = self.get_wifi_iface(dev, key_name)
        return rtnval

    def get_log_level(self, dev) -> int:
        """
            Get the log_level. Supported levels are:
                0 = verbose debugging
                1 = debugging,
                2 = informational messages
                3 = notification
                4 = warning

            :param dev: the wifi device index to set the region on
        """
        rtnval = self.get_radio(dev, 'log_level')
        return rtnval

    def get_logs(self, clear: bool=False) -> str:
        """
            Get the OpenWRT logs using the logread command

            :param clear: clear the log

            :returns: Output of the logread command
        """
        command = 'logread'
        status, stdout, stderr = self._ssh_run_command(command)
        if status == 0:
            if clear:
                # Restart the logging daemon to clear the logs
                clear_command = '/etc/init.d/log restart'
                status, stdout, stderr = self._ssh_run_command(clear_command)
                if status != 0:
                    errmsg ="Failure clearing the daemon log"
                    raise self._create_openwrt_request_error(clear_command, status, stdout, stderr, errmsg)
        else:
            errmsg ="Failure reading log for"
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return stdout

    def get_macaddr(self, dev: int) -> str:
        """
            Gets the override MAC address used for the wifi interface.

            :param dev: the wifi device index to set the region on

            :returns: the mac address to use for an override address
        """
        rtnval = self.get_wifi_iface(dev, 'macaddr')
        return rtnval

    def get_macfilter(self, dev: int) -> str:
        """
            Gets the specified the mac filter policy, disable to disable the filter, allow to
            treat it as whitelist or deny to treat it as blacklist.
            
            ..note: Supported for the mac80211 since r25105
                    AP default = disable

            :param dev: the wifi device index to set the region on
        """
        rtnval = self.get_radio(dev, 'macfilter')
        return rtnval

    def get_maclist(self, dev: int) -> str:
        """
            Gets the list of MAC addresses to put into the mac filter.

            ..note: Supported for the mac80211 since r25105

            :param dev: the wifi device index to set the region on
        """
        rtnval  = self.get_radio(dev, 'maclist')
        return rtnval

    def get_max_listen_int(self, dev: int) -> int:
        """
            Gets the maximum allowed STA (client) listen interval. Association will be
            refused if a STA attempts to associate with a listen interval greater than
            this value. This option only has an effect on ap wifi-ifaces.
            
            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on

            :returns: the maximum allowed client listen interval
        """
        rtnval = self.get_wifi_iface(dev, 'max_listen_int')
        return rtnval

    def get_maxassoc(self, dev: int) -> int:
        """
            Gets the specified maximum number of clients to connect.

            :param dev: the wifi device index to set the region on

            :returns: the max number of clients 
        """
        rtnval = self.get_wifi_iface(dev, 'maxassoc')
        return rtnval

    def get_mcast_rate(self, dev: int) -> int:
        """
            Gets the fixed multicast rate, measured in kb/s.
        
            ..note: Only supported by madwifi, and mac80211 (for type adhoc)

            :param dev: the wifi device index to set the region on

            :returns: the fixed multicast rate in kb/s
        """
        rtnval = self.get_wifi_iface(dev, 'mcast_rate')
        return rtnval

    def get_mode(self, dev: int) -> str:
        """
            Selects the operation mode of the wireless network, ap for Access Point, sta for
            managed (client) mode, adhoc for Ad-Hoc, wds for static WDS and monitor for monitor
            mode, mesh for 802.11s mesh mode.

            ..note: mesh mode only supported by mac80211

            :param dev: the wifi device index to set the region on
            
            :returns: the operation mode of the radio
        """
        rtnval = self.get_wifi_iface(dev, 'mode')
        return rtnval

    def get_model_name(self) -> str:
        """
            Get the OpenWRT model name
        """
        if self._model_name is None:
            command = 'cat /etc/openwrt_release'
            status, stdout, stderr = self._ssh_run_command(command)
            if status == 0:
                m = re.search(r"DISTRIB_TARGET='(.+)/", stdout)

                if m is not None:
                    self._model_name = m.group(1)  # cache the model name
                else:
                    errmsg ="Failure parsing model name"
                    raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)
            else:
                errmsg ="Failure retrieving model information."
                raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return self._model_name

    def get_network(self, dev: int) -> str:
        """
            Specifies the network interface to attach the wireless to.
            lan, wan, etc.

            :param dev: the wifi device index to set the region on

            :returns: the network interface
        """
        rtnval = self.get_wifi_iface(dev, 'network')
        return rtnval

    def get_noscan(self, dev:int) -> bool:
        """
            Do not scan for overlapping BSSs in HT40+/- mode.
            
            ..note: Only supported by mac80211 Turning this on will
                violate regulatory requirements!

            :param dev: the wifi device index to set the region on
        """
        rtnval = self.get_radio(dev, 'noscan')
        return rtnval

    def get_openwrt_version(self) -> str:
        """
            Get the OpenWRT version as a tuple containing maj, min, patch
        """
        if self._openwrt_version is None:
            command = 'cat /etc/openwrt_release'
            status, stdout, stderr = self._ssh_run_command(command)
            if status == 0:
                m = re.search(r"DISTRIB_RELEASE='(\d+)\.(\d+)\.(\d+)'", stdout)

                if m is not None:
                    self._openwrt_version = map(int, m.groups())
                else:
                    errmsg ="Failure parsing openwrt_release version."
                    raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)
            else:
                errmsg ="Failure retrieving openwrt_release information."
                raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return self._openwrt_version

    def get_radio(self, dev: int, parameter: str):
        """
            Gets configuration settings related to the wireless radio's in the AP.

            :param dev: device (0 or 1)
            :param parameter: parameter being configured

            :returns: the configuration setting for the given radio parameter
        """
        prop_name = 'wireless.radio{}.{}'.format(dev, parameter)
        rtnval = self.uci_get(prop_name)
        return rtnval

    def get_region(self, dev: int):
        """
            Retrieve the currently-configured region for BSSID specified by dev

            :param dev: the wifi device index to get the region from
            
            :returns: 2-character country code
        """
        rtnval = DEFAULT_REGION_CODE

        country_code_found = self.get_radio(dev, 'country')

        if 'uci: Entry not found' not in country_code_found:
            rtnval =  country_code_found

        return rtnval

    def get_rxantenna(self, dev: int) -> int:
        """
            Specifies the antenna for receiving, the value may be driver specific,
            usually it is 1 for the first and 2 for the second antenna. Specifying 0
            enables automatic selection by the driver if supported. This option has
            no effect if diversity is enabled.

            ..note: AP default = Driver default

            :param dev: the wifi device index to set the region on
        """
        rtnval = self.get_radio(dev, 'rxantenna')
        return rtnval

    def get_ssid(self, dev: int) -> str:
        """
            The broadcasted SSID of the wireless network (for managed mode the SSID of the network
            you're connecting to).

            :param dev: the wifi device index to set the region on

            :returns: the ssid to broadcast
        """
        rtnval = self.get_wifi_iface(dev, 'ssid')
        return rtnval

    def get_supported_wifi_channels(self, dev: int) -> Tuple[WifiChannelInfo]:
        """
            Gets the supported WiFi channels for this device

            :param dev: the wifi device index

            :returns: list of supported frequencies and channels
        """
        rtnval = None

        radio_index = self.get_2ghz_radio_index()
        if dev == radio_index:
            rtnval = G_CHANNEL_MAPPING[:12]
        else:
            rtnval = N_CHANNEL_MAPPING

        return rtnval

    def get_txantenna(self, dev: int):
        """
            Gets the specified antenna for transmitting, values are identical to rxantenna.
            ..note: AP default = Driver default

            :param dev: the wifi device index to set the region on
        """
        rtnval = self.get_radio(dev, 'txantenna')
        return rtnval

    def get_txpower(self, dev: int):
        """
            Gets the specified transmission power in dB.
            
            ..note: AP default =  driver default

            :param dev: the wifi device index to set the region on
        """
        rtnval = self.get_radio(dev, 'txpower')
        return rtnval

    def get_wep_rekey(self, dev: int) -> int:
        """
            Gets the specified rekey interval in seconds.

            :param dev: the wifi device index to set the region on

            :returns: rekey interval in seconds
        """
        rtnval = self.get_wifi_iface(dev, 'wep_rekey')
        return rtnval

    def get_wifi_iface(self, dev: int, parameter: str) -> Any:
        """
        Gets configuration settings related to the wireless interfaces in the AP.

        :param dev: device (0 or 1)
        :param parameter: parameter being configured

        :returns: the configuration setting for the given wireless interface parameter
        """
        rtnval = self.uci_get('wireless.@wifi-iface[{}].{}'.format(dev, parameter))
        return rtnval

    def get_wmm(self, dev: int) -> int:
        """
            Returns wmm setting on the device interface

            :param dev: the wifi device index to set the region on
        
            :returns: 1 for wmm enabled or 0 for wmm disabled
        """
        rtnval = self.get_wifi_iface(dev, 'wmm')
        return rtnval

    def get_wpa_group_rekey(self, dev: int) -> int:
        """
            Gets the specified the rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param wpa_group_rekey: the wpa group rekey interval
        """
        rtnval = self.get_wifi_iface(dev, 'wpa_group_rekey')
        return rtnval

    def get_wpa_pair_rekey(self, dev: int) -> int:
        """
            Gets the specified rekey interval in seconds

            :param dev: the wifi device index to set the region on
            
            :returns: the wpa pair rekey interval
        """
        rtnval = self.get_wifi_iface(dev, 'wpa_pair_rekey')
        return rtnval

    def get_wps_device_name(self, dev: int) -> str:
        """
            Gets the wps_devicename string

            :param dev: the wifi device index to set the region on

            :returns: string to set for the WPS device name IE
        """
        rtnval = self.get_wifi_iface(dev, 'wps_device_name')
        return rtnval

    def get_wps_manufacturer(self, dev: int) -> str:
        """
            Gets the wps_manufacturer string

            :param dev: the wifi device index to set the region on
            :param value: string to set for the WPS manufacturer IE
        """
        rtnval = self.get_wifi_iface(dev, 'wps_manufacturer')
        return rtnval

    def get_wps_pushbutton(self, dev: int) -> int:
        """
            Gets the wps_pushbutton config to be either 1 or 0

            :param dev: the wifi device index to set the region on

            :returns: value to set wps_pushbutton to
        """
        rtnval = self.get_wifi_iface(dev, 'wps_pushbutton')
        return rtnval

    def is_channel_supported(self, dev: int, channel: int) -> bool:
        """
            Test if a channel is supported by wifi device dev

            :param dev: the wifi device index
            :param channel: Channel to check (index or frequency)
            
            :returns: channel is supported
        """
        rtnval = False

        if channel == 'auto':
            rtnval = True
        else:
            matching_channels = [channel_info for channel_info in self.get_supported_wifi_channels(dev) if channel in channel_info]
            rtnval = any(matching_channels)

        return rtnval

    def mark_log(self, msg):
        """
            Mark the OpenWRT log with a custom message
        """
        command = 'logger {}'.format(msg)
        status, stdout, stderr = self._ssh_run_command(command)
        if status != 0:
            errmsg ="Failure attempting to mark the log."
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)
        return


    def ping(self, host: str, count: int):
        """
            Ping device from OpenWrt AP

            :param host: device to ping (ip or hostname)
            :param count: number of ICMP requests
            
            :returns: ping result returned from _ssh session

            TODO: Return int with ICMP requests received
        """
        command = 'ping -q -c {} {}'.format(count, host)

        status, stdout, stderr = self._ssh_run_command(command)
        if status == 0:
            ping_lines = stdout.splitlines()
            if len(ping_lines) > 0:
                rcvd_lines = [line for line in ping_lines if 'received' in line]
                if len(rcvd_lines) > 0:
                    line_parts = rcvd_lines[0].split(' ')
                    replies = int(line_parts[3])

        return replies

    def restart_wifi(self):
        """
            Restart the wireless radio's

            :raises:
                AKitOpenWRTRequestError - if any problems were encountered during restart
        """
        RESTART_TIMEOUT_SEC = 15
        RESTART_AVG_SEC = 8  # On average, wifi init takes around 7-8 seconds

        command = "wifi"
        status, stdout, stderr = self._ssh_run_command(command)
        if status == 0:
            time.sleep(RESTART_AVG_SEC)

            # search all words output from wifi command for common config error
            # indicators
            restart_words = stdout.split()
            if set(restart_words) & self.SET_OF_WIFI_RESTART_ERRORS_TERMS:
                errmsg = 'Error restarting Wi-Fi'
                raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)
        else:
            errmsg = 'Error running command to restart Wi-Fi'
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return

    def reset_wifi_config(self):
        """
            Reset the wifi configuration to factory defaults on the OpenWrt AP
        """
        command = 'rm -f /etc/config/wireless; wifi config > /etc/config/wireless'
        status, stdout, stderr = self._ssh_run_command(command)
        if status != 0:
            errmsg = 'Error resetting wifi config to defaults.'
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        self.commit_wifi_config_and_restart_radios()

        return

    def set_basic_rate(self, dev: int, basic_rate: int):
        """
            Set the supported basic rates. Each basic_rate is measured in kb/s.
            This option only has an effect on ap and adhoc wifi-ifaces.
            
            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param basic_rate: The basic rate to set
        """
        self.set_radio(dev, 'basic_rate', basic_rate)
        return

    def set_beacon_int(self, dev: int, beacon_int: int):
        """
            Set the beacon interval. This is the time interval between beacon
            frames, measured in units of 1.024 ms. hostapd permits this to be
            set between 15 and 65535. This option only has an effect on ap
            and adhoc wifi-ifaces.
            
            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param beacon_int: the beacon interval
        """
        self.set_radio(dev, 'beacon_int', beacon_int)
        return

    def set_channel(self, dev: int, channel: int):
        """
            Specifies the wireless channel to use. In station mode the value auto
            is allowed, in access point mode an actual channel number must be
            given

            :param dev: the wifi device to set the channel on
            :param channel: the channel number to set
            
            :raises ValueError: if the channel provided is unsupported for the wireless device
        """
        if not self._is_supported_channel(dev, channel):
            raise ValueError(
                "channel <{}> is unsupported, please use one of: {}".format(
                    channel, [
                        channel_info.channel for channel_info in
                        self.get_supported_wifi_channels(dev)]))

        self.set_radio(dev, 'channel', channel)
        return

    def set_disabled(self, dev: int, disabled: bool):
        """
            Disables the radio adapter if set to 1. Setting it to 0 will enable the adapter.

            :param dev: the radio (0 or 1)
            :param disabled: boolean indicating the disabled state

            ..note: AP default = 1

        """
        self.set_radio(dev, 'disabled', disabled)
        return

    def set_diversity(self, dev: int, diversity: bool):
        """
            Enables or disables the automatic antenna selection by the driver.
            Note: AP default = 1

            :param dev: the wifi device index to set the region on
            :param diversity: a boolean turning on or off diversity
        """
        self.set_radio(dev, 'diversity', diversity)
        return

    def set_dtim_period(self, dev: int, dtim_period: int):
        """
            Set the DTIM (delivery traffic information message) period. There will
            be one DTIM per this many beacon frames. This may be set between 1 and
            255. This option only has an effect on ap wifi-ifaces.

            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param dtim_period: the delivery traffic information message period
        """
        self.set_wifi_iface(dev, 'dtim_period', dtim_period)
        return

    def set_encryption(self, dev: int, encryption: str):
        """
            Wireless encryption method. none for an open network, wep for WEP, psk for WPA-PSK,
            or psk2 for WPA2-PSK. See the WPA modes below for additional possible values.
            For an access point in WEP mode, the default is "open system" authentication. Use
            wep+shared for "shared key" authentication (less secure), wep+open to explicitly use
            "open system," or wep+mixed to allow either. wep+mixed is only supported by hostapd.

            :param dev: the wifi device index to set the region on
            :param encryption: the encryption method

                WEP Values
                    wep+shared
                    wep+open
                WPA Values
                    psk2+tkip+ccmp      -> PTK=CCMP GTK=TKIP
                    psk2+tkip           -> PTK=CCMP GTK=TKIP
                    psk2+ccmp           -> PTK=CCMP GTK=CCMP
                    psk+tkip+ccmp       -> PTK=CCMP GTK=TKIP
                    psk+tkip            -> PTK=TKIP GTK=TKIP
                    psk+ccmp            -> PTK=CCMP GTK=CCMP
                    mixed-psk+tkip+ccmp -> PTK=CCMP GTK=TKIP
                    mixed-psk+tkip      -> PTK=TKIP GTK=TKIP
                    mixed-psk+ccmp      -> PTK=CCMP GTK=CCMP
        """
        self.set_wifi_iface(dev, 'encryption', encryption)
        return

    def set_fragmentation_threshold(self, dev: int, frag_size: int):
        """
            Sets the WiFi frame fragmentation threshold for a given radio

            :param dev: the radio (0 or 1)
            :param frag_size - an integer representing the fragmentation threshold size
        """
        self.set_radio(dev, 'frag', frag_size)
        return

    def set_hidden(self, dev: int, hidden: str):
        """
            Turns off SSID broadcasting if set to 1

            :param dev: the wifi device index to set the region on
            :param hidden: boolean indicating if the ssid is hidden
        """
        self.set_wifi_iface(dev, 'hidden', hidden)
        return

    def set_hwmode(self, dev, hwmode):
        """
            Selects the wireless protocol to use, possible values are 11b, 11bg, 11g,
            11gdt (G + dynamic turbo, madwifi only), 11gst (G turbo, broadcom only), 11a,
            11adt (A + dynamic turbo, madwifi only), 11ast (A + static turbo, madwifi only),
            11fh (frequency hopping), 11lrs (LRS mode, broadcom only), 11ng (11N+11G, 2.4GHz,
            mac80211 only), 11na (11N+11A, 5GHz, mac80211 only) or auto.
            
            ..note: AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param hwmode: the hardware mode to set for the device provided.

        """
        self.set_radio(dev, 'hwmode', hwmode)
        return

    def set_ht_capab(self, dev, ht_capab):
        """
            Specifies the available capabilities of the radio. The values are autodetected.
            This option is only used for type mac80211.
            
            ..note: mac80211 is the default, we never change this.
                    AP default =  driver default
            
            :param dev: the wifi device index to set the region on
            :param ht_capab: specifies the ht_capab to set.
        """
        self.set_radio(dev, 'ht_capab', ht_capab)
        return

    def set_htmode(self, dev: int, htmode: int):
        """
            Specifies the channel width in 11ng and 11na mode, possible values are: HT20
            (single 20MHz channel), HT40- (2x 20MHz channels, primary/control channel is upper,
            secondary channel is below) or HT40+ (2x 20MHz channels, primary/control channel is
            lower, secondary channel is above. This option is only used for type mac80211.

            ..note: mac80211 is the default, we never change this.
                    AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param htmode: the htmode to set
        """
        self.set_radio(dev, 'htmode', htmode)
        return

    def set_ieee80211w(self, dev:int, fpval: int):
        """
            Sets the management frame protection (802.11w) value

            ..note:: AP should be set for some wpa-psk encryptiopn setting in order for
                     ieee80211w to be set to some non-zero value.

            :param dev: the wifi device index to set the region on
            :param fpval: value to set for 802.11w, which has the following
                          meaning for openwrt: 2=required, 1=optional,
                          0=802.11w is disabled (same as ieee80211w setting being absent)
        """
        self.set_wifi_iface(dev, 'ieee80211w', fpval)
        return

    def set_isolate(self, dev: int, isolate: bool):
        """
            Isolate wireless clients from each other, only applicable in ap mode.
            Note: May not be supported in the original Backfire release for mac80211.

            :param dev: the wifi device index to set the region on
            :param isolate: A boolean indicating to isolate wireless clients
        """
        self.set_wifi_iface(dev, 'isolate', isolate)
        return

    def set_key(self, dev: int, key: Union[int, str], key_ordinal: Optional[int]=None):
        """
            In any WPA-PSK mode, this is a string that specifies the pre-shared passphrase from
            which the pre-shared key will be derived. If a 64-character hexadecimal string is
            supplied, it will be used directly as the pre-shared key instead.
            In WEP mode, this can be an integer specifying which key index to use (key1, key2, key3,
            or key4.) Alternatively, it can be a string specifying a passphrase or key directly, as in key1.
            In any WPA-Enterprise AP mode, this option has a different interpretation.

            :param dev: the wifi device index to set the region on
            :param key: the key information integer key (WEP mode), string key (wpa-psk mode)
            :param key_ordinal: the ordinal to append to the key name
        """
        key_name = 'key'
        if key_ordinal is not None:
            key_name += str(key_ordinal)

        self.set_wifi_iface(dev, key_name, key)
        return

    def set_log_level(self, dev: int, log_level: int):
        """
            Set the log_level. Supported levels are:
                0 = verbose debugging
                1 = debugging,
                2 = informational messages
                3 = notification
                4 = warning

            :param dev: the wifi device index to set the region on
            :param log_level: The log level
        """
        self.set_radio(dev, 'log_level', log_level)
        return

    def set_macaddr(self, dev: int, macaddr: str):
        """
            Overrides the MAC address used for the wifi interface.

            :param dev: the wifi device index to set the region on
            :param macaddr: the mac address to use for an override address
        """
        self.set_wifi_iface(dev, 'macaddr', macaddr)
        return

    def set_macfilter(self, dev: int, macfilter: str):
        """
            Specifies the mac filter policy, disable to disable the filter, allow to
            treat it as whitelist or deny to treat it as blacklist.
            
            ..note: Supported for the mac80211 since r25105
                    AP default = disable

            :param dev: the wifi device index to set the region on
            :param macfilter: (enable\disable)
        """
        self.set_radio(dev, 'macfilter', macfilter)
        return

    def set_maclist(self, dev: int, maclist: str):
        """
            Sets the list of MAC addresses to put into the mac filter.

            ..note: Supported for the mac80211 since r25105

            :param dev: the wifi device index to set the region on
            :param maclist: List of space-separated mac addresses to allow/deny
                            according to wl0_macmode. Enter addresses with colons, e.g.:
                            "00:02:2D:08:E2:1D 00:03:3E:05:E1:1B" and put them in quotes if
                            you have more than one mac
        """
        self.set_radio(dev, 'maclist', maclist)
        return

    def set_max_listen_int(self, dev: int, max_listen_int: int):
        """
            Set the maximum allowed STA (client) listen interval. Association will be
            refused if a STA attempts to associate with a listen interval greater than
            this value. This option only has an effect on ap wifi-ifaces.
            
            ..note: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param max_listen_int: the maximum allowed client listen interval
        """
        self.set_wifi_iface(dev, 'max_listen_int', max_listen_int)
        return

    def set_maxassoc(self, dev: int, maxassoc: int):
        """
            Specifies the maximum number of clients to connect.

            :param dev: the wifi device index to set the region on
            :param maxassoc: the max number of clients 
        """
        self.set_wifi_iface(dev, 'maxassoc', maxassoc)
        return

    def set_mcast_rate(self, dev: int, mcast_rate: int):
        """
            Sets the fixed multicast rate, measured in kb/s.
            
            ..note: Only supported by madwifi, and mac80211 (for type adhoc)

            :param dev: the wifi device index to set the region on
            :param mcast_rate: the fixed multicast rate in kb/s
        """
        self.set_wifi_iface(dev, 'mcast_rate', mcast_rate)
        return

    def set_mode(self, dev: int, mode: str):
        """
            Selects the operation mode of the wireless network, ap for Access Point, sta for
            managed (client) mode, adhoc for Ad-Hoc, wds for static WDS and monitor for monitor
            mode, mesh for 802.11s mesh mode.

            ..note: mesh mode only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param mode: the operation mode of the radio
        """
        self.set_wifi_iface(dev, 'mode', mode)
        return

    def set_network(self, dev: int, network: str):
        """
            Specifies the network interface to attach the wireless to.
            lan, wan, etc.

            :param dev: the wifi device index to set the region on
            :param network: the network interface
        """
        self.set_wifi_iface(dev, 'network', network)
        return

    def set_noscan(self, dev:int, noscan: bool):
        """
            Do not scan for overlapping BSSs in HT40+/- mode.
            
            ..note: Only supported by mac80211 Turning this on will
                violate regulatory requirements!

            :param dev: the wifi device index to set the region on
            :param noscan: boolean indicating to not scan
        """
        self.set_radio(dev, 'noscan', noscan)
        return

    def set_radio(self, dev: int, parameter: str, value: str):
        """
            Set radio configuration option on OpenWrt AP.
            If no value is passed for a given param then the option is deleted.

            :param dev: device (0 or 1)
            :param parameter: parameter being configured
            :param value: - setting for parameter
        """
        prop_name = 'wireless.radio{}.{}'.format(dev, parameter)
        self.uci_set(prop_name, value)
        return

    def set_region(self, dev: int, country_code: str):
        """
        Specifies the wireless region to use. Region is specified using the 2-character country code.

        :param dev: the wifi device index to set the region on
        :param country_code: two-character region code
        
        .. note::
            Region code modifications shall only be made on APs located in
            isolation chambers or screen rooms.

        """
        if country_code not in REGION_CODES:
            raise ValueError("Invalid country code: {}".format(country_code))

        self.set_radio(dev, 'country', country_code)
        return

    def set_rxantenna(self, dev: int, rxantenna: int):
        """
            Specifies the antenna for receiving, the value may be driver specific,
            usually it is 1 for the first and 2 for the second antenna. Specifying 0
            enables automatic selection by the driver if supported. This option has
            no effect if diversity is enabled.

            ..note: AP default = Driver default

            :param dev: the wifi device index to set the region on
            :param rxantenna: index of the receive antenna
        """
        self.set_radio(dev, 'rxantenna', rxantenna)
        return

    def set_ssid(self, dev: int, ssid: str):
        """
            The broadcasted SSID of the wireless network (for managed mode the SSID of the network
            you're connecting to).

            :param dev: the wifi device index to set the region on
            :param ssid: the ssid to broadcast
        """
        self.set_wifi_iface(dev, 'ssid', ssid)
        return

    def set_txantenna(self, dev: int, txantenna: int):
        """
            Specifies the antenna for transmitting, values are identical to rxantenna.
            ..note: AP default = Driver default

            :param dev: the wifi device index to set the region on
            :param txantenna: index of the receive antenna
        """
        self.set_radio(dev, 'txantenna', txantenna)
        return

    def set_txpower(self, dev: int, txpower: int):
        """
            Specifies the transmission power in dB.
            
            ..note: AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param txpower: the transmission power
        """
        return self.set_radio(dev, 'txpower', txpower)

    def set_wep_rekey(self, dev: int, wep_rekey: int):
        """
            Specifies the rekey interval in seconds.

            :param dev: the wifi device index to set the region on
            :param wep_rekey: rekey interval in seconds
        """
        self.set_wifi_iface(dev, 'wep_rekey', wep_rekey)
        return

    def set_wifi_iface(self, dev: int, parameter: str, value: str):
        """
            Set wireless interface configuration setting on OpenWrt AP
            If no value is passed for a given param then the option is deleted.

            :param dev: the wifi device index to set the region on
            :param parameter: parameter being configured
            :param value: setting for parameter
        """
        prop_name = 'wireless.@wifi-iface[{}].{}'.format(dev, parameter)
        rtnval = self.uci_set(prop_name, value)
        return rtnval

    def set_wmm(self, dev: int, enabled_state: int):
        """
            Enables/disables wmm support.

            :param dev: the wifi device index to set the region on
            :param enabled_state: 1 or 0 for enabled or disabled
        """
        self.set_wifi_iface(dev, 'wmm', enabled_state)
        return

    def set_wpa_group_rekey(self, dev: int, wpa_group_rekey: int):
        """
            Specifies the rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param wpa_group_rekey: the wpa group rekey interval
        """
        self.set_wifi_iface(dev, 'wpa_group_rekey', wpa_group_rekey)
        return

    def set_wpa_pair_rekey(self, dev: int, wpa_pair_rekey: int):
        """
            Specifies the rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param wpa_pair_rekey: the wpa pair rekey interval
        """
        self.set_wifi_iface(dev, 'wpa_pair_rekey', wpa_pair_rekey)
        return

    def set_wps_device_name(self, dev: int, dev_name: str):
        """
            Sets the wps_devicename string

            :param dev: the wifi device index to set the region on
            :param dev_name: string to set for the WPS device name IE
        """
        self.set_wifi_iface(dev, 'wps_device_name', dev_name)
        return

    def set_wps_manufacturer(self, dev: int, manufacturer: str):
        """
            Gets the wps_manufacturer string

            :param dev: the wifi device index to set the region on
            :param manufacturer: string to set for the WPS manufacturer IE
        """
        self.set_wifi_iface(dev, 'wps_manufacturer', manufacturer)
        return

    def set_wps_pushbutton(self, dev: int, pbval: int):
        """
            Sets the wps_pushbutton config to be either 1 or 0

            :param dev: the wifi device index to set the region on
            :param pbval: value to set wps_pushbutton to
        """
        self.set_wifi_iface(dev, 'wps_pushbutton', pbval)
        return


# ============================================================================================================
# ============================================================================================================
# ============================================================================================================
# ============================================================================================================
# ============================================================================================================



# ============================================================================================================
# ============================================================================================================
# ============================================================================================================
# ============================================================================================================
# ============================================================================================================




    def uci_delete(self, prop_name: str, aspects: Aspects=None):
        """
            Issues a 'uci delete' command to remove a configuration property

            :param prop_name: the router configuration property string
        """
        if aspects is None:
            aspects = self._aspects

        command = "uci delete {}".format(prop_name)
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects)
        if status != 0:
            errmsg_lines = [
                "Error deleting router configuration property name={}.",
                "COMMAND: {}".format(command),
                "STDOUT: {}".format(stdout),
                "STDERR: {}".format(stderr)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitOpenWRTRequestError(errmsg)

        return

    def uci_get(self, prop_name: str, aspects: Aspects=None) -> str:
        """
            Issues the 'uci get' command to retrieve a value for a given property.
            Note: Converts integers and decimals to their respective primitives.

            :param prop_name: the router configuration property string

            :returns: the value returned by uci
        """
        if aspects is None:
            aspects = self._aspects

        command = "uci get {}".format(prop_name)
        
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects)
        if status != 0:
            errmsg_lines = [
                "Error getting router configuration property name={}.",
                "COMMAND: {}".format(command),
                "STDOUT: {}".format(stdout),
                "STDERR: {}".format(stderr)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitOpenWRTRequestError(errmsg)

        return stdout

    def uci_set(self, prop_name: str, prop_value: str, aspects: Aspects=None):
        """
            Issues a 'uci set' command to change a configuration property

            ..note: if the ' character is used in value it is automatically escaped
                    with the default UCI_ESCAPE_CHAR sequence for the AP

            :param prop_name: the router configuration property string
            :param prop_value: the value you wish to set param to or None if
                               you want to delete param
        """
        if aspects is None:
            aspects = self._aspects

        command = "uci set {} {}".format(prop_name, prop_value)
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects)
        if status != 0:
            errmsg_lines = [
                "Error getting router configuration property name={}.",
                "COMMAND: {}".format(command),
                "STDOUT: {}".format(stdout),
                "STDERR: {}".format(stderr)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitOpenWRTRequestError(errmsg)

        found_result = self.uci_get(prop_name)
        if found_result != prop_value:
            errmsg_lines = [
                "Error property set did not take place. setto={} found={}.".format(prop_value, found_result)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitOpenWRTRequestError(errmsg)

        return

    def _create_openwrt_request_error(self, command, status, stdout, stderr, msg_template, *args):
        errmsg_lines = [
                msg_template.format(*args) + " {}".format(self),
                "COMMAND: {}".format(command),
                "STATUS: {}".format(status),
                "STDOUT:",
                stdout,
                "STDERR:",
                stderr
            ]
        errmsg = os.linesep.join(errmsg_lines)
        return AKitOpenWRTRequestError(errmsg)

    def _ssh_run_command(self, command: str, exp_status: Union[int, Sequence]=0, user: str = None, pty_params: dict = None, aspects: Optional[Aspects] = None):
        """
            Private helper that will run a command on a remote machine via SSH.  If a ssh session object is
            open, then the session will be used to run the command, if a session is not open then the command
            is run via the normal ssh agent directly.
        """
        
        status, stdout, stderr = None, None, None

        if self._ssh_session is not None:
            status, stdout, stderr = self._ssh_session.run_cmd(command, exp_status=exp_status, user=user, pty_params=pty_params, aspects=aspects)
        else:
            status, stdout, stderr = self._ssh_agent.run_cmd(command, exp_status=exp_status, user=user, pty_params=pty_params, aspects=aspects)

        return status, stdout, stderr

    def _try_convert_primitive(self, val):
        if val:
            try:
                val = int(val)
            except ValueError:
                try:
                    val = float(val)
                except ValueError:
                    pass
        return val

    def __repr__(self):
        """
            Override representation for WirelessAPAgent
        """
        model_name = "unknown"
        if self._model_name is not None:
            model_name = self._model_name
        rtnval = "{}({}-{})".format(type(self).__name__, model_name, self._ssh_agent.ipaddr)
        return rtnval
