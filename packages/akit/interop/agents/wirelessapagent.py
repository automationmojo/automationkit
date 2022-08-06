
from typing import Any, Optional, Sequence, Tuple, Union

import json
import os
import re
import time
import traceback

from akit.exceptions import AKitOpenWRTRequestError

from akit.interop.agents.sshagent import SshAgent, SshSession
from akit.interop.wireless.constants import (
    DeAuthenticationReason, OpenWrtModel,
    DEFAULT_REGION_CODE, REGION_CODES)
from akit.interop.wireless.channels import G_CHANNEL_MAPPING, N_CHANNEL_MAPPING, WifiChannelInfo

from akit.interop.wireless.fastpingresult import FastPingResult
from akit.interop.wireless.stationinfo import StationInfo

from akit.aspects import Aspects, DEFAULT_CMD_ASPECTS
from akit.interop.credentials.sshcredential import SshCredential

from  akit.xlogging.foundations import getAutomatonKitLogger
from interfaces.icommandrunner import ICommandRunner

class WirelessAPAgent:
    """
        The :class:`WirelessApAgent` provides an implementation of a administrative
        interface for devices that are running the OpenWRT wireless router software.
    """

    logger = getAutomatonKitLogger()

    SET_OF_WIFI_RESTART_ERRORS_TERMS = set(('error', 'invalid'))

    def __init__(self, ap_host: str, admin_credential: SshCredential, port: int=22, aspects: Aspects=DEFAULT_CMD_ASPECTS):
        self._ap_host: str = ap_host
        self._admin_credential: SshCredential = admin_credential
        self._port: int = port
        self._aspects: Aspects = aspects

        self._ssh_agent: SshAgent = SshAgent(self._ap_host, self._admin_credential, aspects=aspects, cmd_runner=cmd_runner)

        self._model_name: str = None
        self._openwrt_version: str = None
        return

    def arping_bcast(self, interface: str, count: int, host: str, aspects: Optional[Aspects]=None,
                     cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Send specified count of broadcast arping requests out specified interface

            :param interface: interface requests to egress
            :param count: number of ICMP requests
            :param host: host to broadcast arp requests for
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: integer replies
        """
        replies = 0
        
        command = 'arping -b -I {} -c {} {}'.format(interface, count, host)
        
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
        if status == 0:
            ping_lines = stdout.splitlines()

            if len(ping_lines) > 0:
                rcvd_lines = [line for line in ping_lines if 'Received' in line]
                if len(rcvd_lines) > 0:
                    line_parts = rcvd_lines[0].split(' ')
                    replies = int(line_parts[1])

                    self.logger.debug("Parsed arping broadcast replies as <{}>".format(replies))

        return replies

    def commit_wifi_config(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Commits the current wireless configuration to the save file

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        command = 'uci commit wireless'

        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
        if status != 0:
            errmsg ="Error while committing wireless configuration changes to file."
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return

    def commit_wifi_config_and_restart_wifi(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Commits the current wifi configuration settings and restarts the wifi radio's.

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.commit_wifi_config(aspects=aspects, cmd_runner=cmd_runner)
        self.restart_wifi(aspects=aspects, cmd_runner=cmd_runner)
        return

    def configured_channel_is_dfs(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> bool:
        """
            Returns True if current channel is a DFS channel.

            .. note::
                CAC is complete when logread reports "DFS-CAC-COMPLETED", which
                takes roughly 60 seconds.

            :param dev: the index of wifi device to test
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: whether or not current channel is a DFS channel

        """
        rtnval = False

        curr_chan = self.get_channel(dev, aspects=aspects, cmd_runner=cmd_runner)
        for chanmap in N_CHANNEL_MAPPING[4:-5]:
            if curr_chan == chanmap.channel:
                rtnval = True
                break

        return rtnval

    def del_client(self,
                   dev: int,
                   client_mac: str,
                   reason: DeAuthenticationReason=DeAuthenticationReason.PREV_AUTH_NOT_VALID,
                   bantime_ms: int=0, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Tells the openWRT AP to deauthenticate the client_mac device.

            :param dev: network interface
            :param client_mac: mac address of client, including colons.
            :param reason: Deauth reason code
            :param bantime_ms: Prevent client from reconnecting for bantime_ms milliseconds
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        del_client_args = {
            "addr": client_mac,
            "reason": reason,
            "deauth": True,
            "ban_time": bantime_ms
        }

        command = "ubus call hostapd.wlan{} del_client '{}'".format(dev, json.dumps(del_client_args))
        
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
        if status != 0:
            errmsg ="Error trying to deauthenticate dev={} mac={}".format(dev, client_mac)
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return

    def delete_basic_rate(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the supported basic rates setting. Each basic_rate is measured in kb/s.
            This option only has an effect on ap and adhoc wifi-ifaces.
            
            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'basic_rate', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_beacon_int(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the beacon interval

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'beacon_int', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_channel(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes that channel setting for the specified device.

            :param dev: the wifi device to set the channel on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :raises ValueError: if the channel provided is unsupported for the wireless device
        """
        self.delete_radio(dev, 'channel', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_disabled(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete the setting to enable or disable the radio.

            .. note:: AP default = 1

            :param dev: the radio (0 or 1)
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'disabled', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_diversity(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Enables or disables the automatic antenna selection by the driver.

            .. note:: AP default = 1

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'diversity', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_dtim_period(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Clears the DTIM (delivery traffic information message) period.

            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'dtim_period', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_encryption(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete the wireless encryption setting

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'encryption', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_fragmentation_threshold(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Sets the WiFi frame fragmentation threshold for a given radio

            :param dev: the radio (0 or 1)
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'frag', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_hidden(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete the setting for SSID broadcasting if set to 1

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'hidden', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_hwmode(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Selects the wireless protocol to use, possible values are 11b, 11bg, 11g,
            11gdt (G + dynamic turbo, madwifi only), 11gst (G turbo, broadcom only), 11a,
            11adt (A + dynamic turbo, madwifi only), 11ast (A + static turbo, madwifi only),
            11fh (frequency hopping), 11lrs (LRS mode, broadcom only), 11ng (11N+11G, 2.4GHz,
            mac80211 only), 11na (11N+11A, 5GHz, mac80211 only) or auto.
            
            .. note:: AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'hwmode', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_htmode(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the channel width in 11ng and 11na mode, possible values are: HT20
            (single 20MHz channel), HT40- (2x 20MHz channels, primary/control channel is upper,
            secondary channel is below) or HT40+ (2x 20MHz channels, primary/control channel is
            lower, secondary channel is above. This option is only used for type mac80211.

            .. note:: mac80211 is the default, we never change this.
                    AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'htmode', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_ht_capab(self, dev, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the available capabilities of the radio. The values are autodetected.
            This option is only used for type mac80211.
            
            .. note:: mac80211 is the default, we never change this.
                    AP default =  driver default
            
            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'ht_capab', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_ieee80211w(self, dev:int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Clears the management frame protection (802.11w) value

            ..note:: AP should be set for some wpa-psk encryptiopn setting in order for
                     ieee80211w to be set to some non-zero value.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'ieee80211w', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_isolate(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Isolate wireless clients from each other, only applicable in ap mode.
            Note: May not be supported in the original Backfire release for mac80211.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'isolate', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_key(self, dev: int, key_ordinal: Optional[int]=None, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Get key parameter. In wep mode, returns index, wpa mode, returns passphrase

            :param dev: the wifi device index to set the region on
            :param key_ordinal: the ordinal to append to the key name
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        key_name = 'key'
        if key_ordinal is not None:
            key_name += str(key_ordinal)

        self.delete_wifi_iface(dev, key_name, aspects=aspects, cmd_runner=cmd_runner)
        return


    def delete_log_level(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete the log_level setting. Supported levels are:
                0 = verbose debugging
                1 = debugging,
                2 = informational messages
                3 = notification
                4 = warning

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'log_level', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_macaddr(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the override MAC address used for the wifi interface.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'macaddr', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_macfilter(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the specified the mac filter policy, disable to disable the filter, allow to
            treat it as whitelist or deny to treat it as blacklist.

            .. note:: Supported for the mac80211 since r25105
                    AP default = disable

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'macfilter', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_maclist(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the list of MAC addresses to put into the mac filter.

            .. note:: Supported for the mac80211 since r25105

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'maclist', aspects=aspects, cmd_runner=cmd_runner)
        return


    def delete_max_listen_int(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Clears the maximum allowed STA (client) listen interval. Association will be
            refused if a STA attempts to associate with a listen interval greater than
            this value. This option only has an effect on ap wifi-ifaces.

            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'max_listen_int', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_maxassoc(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the specified maximum number of clients to connect.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'maxassoc', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_mcast_rate(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Clears the fixed multicast rate, measured in kb/s.
            
            .. note:: Only supported by madwifi, and mac80211 (for type adhoc)

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'mcast_rate', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_mode(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the selecttion for the operation mode of the wireless network, ap for
            Access Point, sta for managed (client) mode, adhoc for Ad-Hoc, wds for static
            WDS and monitor for monitor mode, mesh for 802.11s mesh mode.

            .. note:: mesh mode only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'mode', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_network(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the network interface to attach the wireless to.
            lan, wan, etc.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'network', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_noscan(self, dev:int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete the do not scan for overlapping BSSs in HT40+/- mode.
            
            .. note:: Only supported by mac80211 Turning this on will
                violate regulatory requirements!

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'noscan', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_radio(self, dev: int, parameter: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            delete radio configuration option on OpenWrt AP.
            If no value is passed for a given param then the option is deleted.

            :param dev: device (0 or 1)
            :param parameter: parameter being configured
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        prop_name = 'wireless.radio{}.{}'.format(dev, parameter)
        self.uci_delete(prop_name, aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_region(self, dev: int, country_code: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
        Delete the wireless region configuration setting.

        :param dev: the wifi device index to set the region on
        :param aspects: The interop aspects to use when engaging with the router commandline interface
        :param cmd_runner: An optional ICommandRunner that is used to run commands.
        
        .. note::
            Region code modifications shall only be made on APs located in
            isolation chambers or screen rooms.

        """
        if country_code not in REGION_CODES:
            raise ValueError("Invalid country code: {}".format(country_code))

        return self.delete_radio(dev, 'country', aspects=aspects, cmd_runner=cmd_runner)

    def delete_rxantenna(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the antenna for receiving, the value may be driver specific,
            usually it is 1 for the first and 2 for the second antenna. Specifying 0
            enables automatic selection by the driver if supported. This option has
            no effect if diversity is enabled.

            .. note:: AP default = Driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'rxantenna', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_ssid(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete the broadcasted SSID of the wireless network (for managed mode the SSID of the network
            you're connecting to).

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'ssid', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_txantenna(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Removes the specified antenna for transmitting, values are identical to rxantenna.
            .. note:: AP default = Driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_radio(dev, 'txantenna', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_txpower(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete the specified the transmission power in dB.
            
            .. note:: AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        return self.delete_radio(dev, 'txpower', aspects=aspects, cmd_runner=cmd_runner)

    def delete_wep_rekey(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the specified rekey interval in seconds.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'wep_rekey', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_wifi_iface(self, dev, param, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete wireless interface configuration setting on OpenWrt AP
            
            :param dev: device (0 or 1)
            :param parameter: parameter being configured
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        prop_name = 'wireless.@wifi-iface[{}].{}'.format(dev, param)
        self.uci_delete(prop_name, aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_wmm(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Clears the wmm setting on the device interface

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'wmm', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_wpa_group_rekey(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Deletes the specified the rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'wpa_group_rekey', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_wpa_pair_rekey(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Delete the specified rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'wpa_pair_rekey', aspects=aspects, cmd_runner=cmd_runner)
        return

    def deletes_wps_device_name(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Gets the wps_devicename string

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'wps_device_name', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_wps_manufacturer(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Clears the wps_manufacturer string

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'wps_manufacturer', aspects=aspects, cmd_runner=cmd_runner)
        return

    def delete_wps_pushbutton(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Clears the wps_pushbutton config to be either 1 or 0

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.delete_wifi_iface(dev, 'wps_pushbutton', aspects=aspects, cmd_runner=cmd_runner)
        return

    def fping(self, host: str, count: int, delay: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> FastPingResult:
        """
            fping device from OpenWrt AP. fping is not istalled by default on image
            and needs to be installed with opkg. Available in packages folder on
            openWrt website.

            :param host: device to ping (ip or hostname)
            :param count: number of ICMP requests
            :param delay: interval between ping packets to one target (in ms)
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: summary results from the fping command
        """
        command = 'fping -q -c {} -p {} {}'.format(count, delay, host)

        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
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

    def get_2ghz_mac_address(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Gets MAC address of the 2ghz radio

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = None

        command = 'ifconfig wlan{}'.format(self.radio_iface_idx_2ghz)
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
        m = re.search('HWaddr (.{17})', stdout)

        if m is not None:
            rtnval = m.group(1).lower()
        else:
            errmsg ="Unable to get 2GHz MAC address"
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return rtnval

    def get_2ghz_radio_index(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            The interface index corresponding the the 2GHz radio

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = None

        model_name = self.get_model_name(aspects=aspects, cmd_runner=cmd_runner)
        if model_name == OpenWrtModel.NETGEAR_7600.value:
            rtnval = 1
        elif model_name in (OpenWrtModel.NETGEAR_WNDR3700.value,
                            OpenWrtModel.NETGEAR_WNDR3700_1907.value):
            rtnval = 0
        else:
            errmsg ="Unsupported Model {}.".format(model_name)
            raise AKitOpenWRTRequestError(errmsg)

        return rtnval

    def get_5ghz_mac_address(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Gets the MAC address of the 5ghz radio

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = None

        command = 'ifconfig wlan{}'.format(self.radio_iface_idx_5ghz)
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
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

    def get_5ghz_radio_index(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the interface index corresponding the the 5GHz radio

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        idx_2ghz = self.get_2ghz_radio_index(aspects=aspects, cmd_runner=cmd_runner)
        rtnval = 0 if idx_2ghz == 1 else 1
        return rtnval

    def get_basic_rate(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Get the supported basic rates. Each basic_rate is measured in kb/s.
            This option only has an effect on ap and adhoc wifi-ifaces.
            
            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param basic_rate: The basic rate to set
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_radio(dev, 'basic_rate', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_beacon_int(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Gets the beacon interval

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: beacon_int
        """
        rtnval = self.get_radio(dev, 'beacon_int', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_channel(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Return the wireless configured channel.

            :param dev: the wifi device index to get the channel for
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the configured channel
        """
        rtnval = self.get_radio(dev, 'channel', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_connected_stations(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> Tuple[StationInfo]:
        """
        Executes the command iw dev station dump on the AP. Output will return detailed
        info on all connected wireless client(s) to the AP.

        :param dev: network interface on AP
        :param aspects: The interop aspects to use when engaging with the router commandline interface
        :param cmd_runner: An optional ICommandRunner that is used to run commands.
        
        :returns: the station dump info as a tuple of

        """
        sta_list = []

        command = 'iw wlan{} station dump'.format(dev)
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)

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

    def get_dtim_period(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the DTIM (delivery traffic information message) period. There will
            be one DTIM per this many beacon frames. This may be set between 1 and
            255. This option only has an effect on ap wifi-ifaces.

            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the delivery traffic information message period
        """
        rtnval = self.get_wifi_iface(dev, 'dtim_period', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_diversity(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> bool:
        """
            Gets whether diversity is enabled or disabled.
            Note: AP default = 1

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: whether diversity is enabled or disabled
        """
        self.get_radio(dev, 'diversity', aspects=aspects, cmd_runner=cmd_runner)
        return

    def get_encryption(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Return wireless encryption setting

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
            
            :returns: the encryption method
        """
        rtnval = self.get_wifi_iface(dev, 'encryption', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_fragmentation_threshold(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the WiFi frame fragmentation threshold for a given radio

            :param dev: the radio (0 or 1)
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the fragmentation size or None if it is not set.
        """
        rtnval = self.get_radio(dev, 'frag', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_hidden(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Delete the setting for SSID broadcasting if set to 1

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_wifi_iface(dev, 'hidden', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_hwmode(self, dev, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Return the hwmode

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: returns the hwmode of the specified device
        """
        rtnval = self.get_radio(dev, 'hwmode', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_ht_capab(self, dev, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Gets the pecified the available capabilities of the radio. The values are autodetected.
            This option is only used for type mac80211.
            
            .. note:: mac80211 is the default, we never change this.
                    AP default =  driver default
            
            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_radio(dev, 'ht_capab', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_htmode(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Specifies the channel width in 11ng and 11na mode, possible values are: HT20
            (single 20MHz channel), HT40- (2x 20MHz channels, primary/control channel is upper,
            secondary channel is below) or HT40+ (2x 20MHz channels, primary/control channel is
            lower, secondary channel is above. This option is only used for type mac80211.

            .. note:: mac80211 is the default, we never change this.
                    AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the htmode to set
        """
        rtnval = self.get_radio(dev, 'htmode', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_ieee80211w(self, dev:int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the management frame protection (802.11w) value

            ..note:: AP should be set for some wpa-psk encryptiopn setting in order for
                     ieee80211w to be set to some non-zero value.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: value to set for 802.11w, which has the following
                      meaning for openwrt: 2=required, 1=optional,
                      0=802.11w is disabled (same as ieee80211w setting being absent)
        """
        rtnval = self.get_wifi_iface(dev, 'ieee80211w', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_isolate(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> bool:
        """
            Isolate wireless clients from each other, only applicable in ap mode.
            Note: May not be supported in the original Backfire release for mac80211.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: A boolean indicating to isolate wireless clients
        """
        rtnval = self.get_wifi_iface(dev, 'isolate', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_key(self, dev: int, key_ordinal: Optional[int]=None, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> Union[int, str]:
        """
            Get key parameter. In wep mode, returns index, wpa mode, returns passphrase

            :param dev: the wifi device index to set the region on
            :param key_ordinal: the ordinal to append to the key name
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the key information integer key (WEP mode), string key (wpa-psk mode)
        """
        key_name = 'key'
        if key_ordinal is not None:
            key_name += str(key_ordinal)

        rtnval = self.get_wifi_iface(dev, key_name, aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_log_level(self, dev, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Get the log_level. Supported levels are:
                0 = verbose debugging
                1 = debugging,
                2 = informational messages
                3 = notification
                4 = warning

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_radio(dev, 'log_level', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_logs(self, clear: bool=False, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Get the OpenWRT logs using the logread command

            :param clear: clear the log
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: Output of the logread command
        """
        command = 'logread'
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
        if status == 0:
            if clear:
                # Restart the logging daemon to clear the logs
                clear_command = '/etc/init.d/log restart'
                status, stdout, stderr = self._ssh_run_command(clear_command, aspects=aspects, cmd_runner=cmd_runner)
                if status != 0:
                    errmsg ="Failure clearing the daemon log"
                    raise self._create_openwrt_request_error(clear_command, status, stdout, stderr, errmsg)
        else:
            errmsg ="Failure reading log for"
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        return stdout

    def get_macaddr(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Gets the override MAC address used for the wifi interface.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the mac address to use for an override address
        """
        rtnval = self.get_wifi_iface(dev, 'macaddr', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_macfilter(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Gets the specified the mac filter policy, disable to disable the filter, allow to
            treat it as whitelist or deny to treat it as blacklist.
            
            .. note:: Supported for the mac80211 since r25105
                    AP default = disable

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_radio(dev, 'macfilter', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_maclist(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Gets the list of MAC addresses to put into the mac filter.

            .. note:: Supported for the mac80211 since r25105

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval  = self.get_radio(dev, 'maclist', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_max_listen_int(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the maximum allowed STA (client) listen interval. Association will be
            refused if a STA attempts to associate with a listen interval greater than
            this value. This option only has an effect on ap wifi-ifaces.
            
            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the maximum allowed client listen interval
        """
        rtnval = self.get_wifi_iface(dev, 'max_listen_int', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_maxassoc(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the specified maximum number of clients to connect.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the max number of clients 
        """
        rtnval = self.get_wifi_iface(dev, 'maxassoc', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_mcast_rate(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the fixed multicast rate, measured in kb/s.
        
            .. note:: Only supported by madwifi, and mac80211 (for type adhoc)

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the fixed multicast rate in kb/s
        """
        rtnval = self.get_wifi_iface(dev, 'mcast_rate', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_mode(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Selects the operation mode of the wireless network, ap for Access Point, sta for
            managed (client) mode, adhoc for Ad-Hoc, wds for static WDS and monitor for monitor
            mode, mesh for 802.11s mesh mode.

            .. note:: mesh mode only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
            
            :returns: the operation mode of the radio
        """
        rtnval = self.get_wifi_iface(dev, 'mode', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_model_name(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Get the OpenWRT model name

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        if self._model_name is None:
            command = 'cat /etc/openwrt_release'
            status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
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

    def get_network(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Specifies the network interface to attach the wireless to.
            lan, wan, etc.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the network interface
        """
        rtnval = self.get_wifi_iface(dev, 'network', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_noscan(self, dev:int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> bool:
        """
            Do not scan for overlapping BSSs in HT40+/- mode.
            
            .. note:: Only supported by mac80211 Turning this on will
                violate regulatory requirements!

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_radio(dev, 'noscan', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_openwrt_version(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Get the OpenWRT version as a tuple containing maj, min, patch

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        if self._openwrt_version is None:
            command = 'cat /etc/openwrt_release'
            status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
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

    def get_radio(self, dev: int, parameter: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Gets configuration settings related to the wireless radio's in the AP.

            :param dev: device (0 or 1)
            :param parameter: parameter being configured
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the configuration setting for the given radio parameter
        """
        prop_name = 'wireless.radio{}.{}'.format(dev, parameter)
        rtnval = self.uci_get(prop_name, aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_region(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Retrieve the currently-configured region for BSSID specified by dev

            :param dev: the wifi device index to get the region from
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
            
            :returns: 2-character country code
        """
        rtnval = DEFAULT_REGION_CODE

        country_code_found = self.get_radio(dev, 'country', aspects=aspects, cmd_runner=cmd_runner)

        if 'uci: Entry not found' not in country_code_found:
            rtnval =  country_code_found

        return rtnval

    def get_rxantenna(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Specifies the antenna for receiving, the value may be driver specific,
            usually it is 1 for the first and 2 for the second antenna. Specifying 0
            enables automatic selection by the driver if supported. This option has
            no effect if diversity is enabled.

            .. note:: AP default = Driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_radio(dev, 'rxantenna', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_ssid(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            The broadcasted SSID of the wireless network (for managed mode the SSID of the network
            you're connecting to).

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the ssid to broadcast
        """
        rtnval = self.get_wifi_iface(dev, 'ssid', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_supported_wifi_channels(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> Tuple[WifiChannelInfo]:
        """
            Gets the supported WiFi channels for this device

            :param dev: the wifi device index
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: list of supported frequencies and channels
        """
        rtnval = None

        radio_index = self.get_2ghz_radio_index(aspects=aspects, cmd_runner=cmd_runner)
        if dev == radio_index:
            rtnval = G_CHANNEL_MAPPING[:12]
        else:
            rtnval = N_CHANNEL_MAPPING

        return rtnval

    def get_txantenna(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Gets the specified antenna for transmitting, values are identical to rxantenna.
            .. note:: AP default = Driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_radio(dev, 'txantenna', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_txpower(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Gets the specified transmission power in dB.
            
            .. note:: AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        rtnval = self.get_radio(dev, 'txpower', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_wep_rekey(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the specified rekey interval in seconds.

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: rekey interval in seconds
        """
        rtnval = self.get_wifi_iface(dev, 'wep_rekey', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_wifi_iface(self, dev: int, parameter: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> Any:
        """
        Gets configuration settings related to the wireless interfaces in the AP.

        :param dev: device (0 or 1)
        :param parameter: parameter being configured
        :param aspects: The interop aspects to use when engaging with the router commandline interface
        :param cmd_runner: An optional ICommandRunner that is used to run commands.

        :returns: the configuration setting for the given wireless interface parameter
        """
        rtnval = self.uci_get('wireless.@wifi-iface[{}].{}'.format(dev, parameter), aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_wmm(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Returns wmm setting on the device interface

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: 1 for wmm enabled or 0 for wmm disabled
        """
        rtnval = self.get_wifi_iface(dev, 'wmm', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_wpa_group_rekey(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the specified the rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param wpa_group_rekey: the wpa group rekey interval
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the rekey interval in seconds
        """
        rtnval = self.get_wifi_iface(dev, 'wpa_group_rekey', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_wpa_pair_rekey(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the specified rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
            
            :returns: the wpa pair rekey interval
        """
        rtnval = self.get_wifi_iface(dev, 'wpa_pair_rekey', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_wps_device_name(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Gets the wps_devicename string

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: string to set for the WPS device name IE
        """
        rtnval = self.get_wifi_iface(dev, 'wps_device_name', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_wps_manufacturer(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Gets the wps_manufacturer string

            :param dev: the wifi device index to set the region on
            :param value: string to set for the WPS manufacturer IE
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the wps manufacturer
        """
        rtnval = self.get_wifi_iface(dev, 'wps_manufacturer', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def get_wps_pushbutton(self, dev: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> int:
        """
            Gets the wps_pushbutton config to be either 1 or 0

            :param dev: the wifi device index to set the region on
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: value to set wps_pushbutton to
        """
        rtnval = self.get_wifi_iface(dev, 'wps_pushbutton', aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def is_channel_supported(self, dev: int, channel: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> bool:
        """
            Test if a channel is supported by wifi device dev

            :param dev: the wifi device index
            :param channel: Channel to check (index or frequency)
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
            
            :returns: channel is supported
        """
        rtnval = False

        if channel == 'auto':
            rtnval = True
        else:
            matching_channels = [channel_info for channel_info in self.get_supported_wifi_channels(dev, aspects=aspects, cmd_runner=cmd_runner) if channel in channel_info]
            rtnval = any(matching_channels)

        return rtnval

    def mark_log(self, msg: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Mark the OpenWRT log with a custom message

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        command = 'logger {}'.format(msg)
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
        if status != 0:
            errmsg ="Failure attempting to mark the log."
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)
        return


    def ping(self, host: str, count: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Ping device from OpenWrt AP

            :param host: device to ping (ip or hostname)
            :param count: number of ICMP requests
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
            
            :returns: ping result returned from _ssh session
        """
        command = 'ping -q -c {} {}'.format(count, host)

        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
        if status == 0:
            ping_lines = stdout.splitlines()
            if len(ping_lines) > 0:
                rcvd_lines = [line for line in ping_lines if 'received' in line]
                if len(rcvd_lines) > 0:
                    line_parts = rcvd_lines[0].split(' ')
                    replies = int(line_parts[3])

        return replies

    def restart_wifi(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Restart the wireless radio's

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :raises:
                AKitOpenWRTRequestError - if any problems were encountered during restart
        """
        RESTART_TIMEOUT_SEC = 15
        RESTART_AVG_SEC = 8  # On average, wifi init takes around 7-8 seconds

        command = "wifi"
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
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

    def reset_wifi_config(self, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Reset the wifi configuration to factory defaults on the OpenWrt AP

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        command = 'rm -f /etc/config/wireless; wifi config > /etc/config/wireless'
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
        if status != 0:
            errmsg = 'Error resetting wifi config to defaults.'
            raise self._create_openwrt_request_error(command, status, stdout, stderr, errmsg)

        self.commit_wifi_config_and_restart_radios()

        return

    def set_basic_rate(self, dev: int, basic_rate: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Set the supported basic rates. Each basic_rate is measured in kb/s.
            This option only has an effect on ap and adhoc wifi-ifaces.
            
            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param basic_rate: The basic rate to set
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'basic_rate', basic_rate, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_beacon_int(self, dev: int, beacon_int: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Set the beacon interval. This is the time interval between beacon
            frames, measured in units of 1.024 ms. hostapd permits this to be
            set between 15 and 65535. This option only has an effect on ap
            and adhoc wifi-ifaces.
            
            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param beacon_int: the beacon interval
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'beacon_int', beacon_int, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_channel(self, dev: int, channel: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the wireless channel to use. In station mode the value auto
            is allowed, in access point mode an actual channel number must be
            given

            :param dev: the wifi device to set the channel on
            :param channel: the channel number to set
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
            
            :raises ValueError: if the channel provided is unsupported for the wireless device
        """
        if not self.is_channel_supported(dev, channel, aspects=aspects, cmd_runner=cmd_runner):
            raise ValueError(
                "channel <{}> is unsupported, please use one of: {}".format(
                    channel, [
                        channel_info.channel for channel_info in
                        self.get_supported_wifi_channels(dev, aspects=aspects, cmd_runner=cmd_runner)]))

        self.set_radio(dev, 'channel', channel)
        return

    def set_disabled(self, dev: int, disabled: bool, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Disables the radio adapter if set to 1. Setting it to 0 will enable the adapter.

            .. note:: AP default = 1

            :param dev: the radio (0 or 1)
            :param disabled: boolean indicating the disabled state
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

        """
        self.set_radio(dev, 'disabled', disabled, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_diversity(self, dev: int, diversity: bool, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Enables or disables the automatic antenna selection by the driver.
            Note: AP default = 1

            :param dev: the wifi device index to set the region on
            :param diversity: a boolean turning on or off diversity
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'diversity', diversity, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_dtim_period(self, dev: int, dtim_period: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Set the DTIM (delivery traffic information message) period. There will
            be one DTIM per this many beacon frames. This may be set between 1 and
            255. This option only has an effect on ap wifi-ifaces.

            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param dtim_period: the delivery traffic information message period
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'dtim_period', dtim_period, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_encryption(self, dev: int, encryption: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
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

            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'encryption', encryption, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_fragmentation_threshold(self, dev: int, frag_size: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Sets the WiFi frame fragmentation threshold for a given radio

            :param dev: the radio (0 or 1)
            :param frag_size - an integer representing the fragmentation threshold size
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'frag', frag_size, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_hidden(self, dev: int, hidden: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Turns off SSID broadcasting if set to 1

            :param dev: the wifi device index to set the region on
            :param hidden: boolean indicating if the ssid is hidden
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'hidden', hidden, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_hwmode(self, dev: int, hwmode: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Selects the wireless protocol to use, possible values are 11b, 11bg, 11g,
            11gdt (G + dynamic turbo, madwifi only), 11gst (G turbo, broadcom only), 11a,
            11adt (A + dynamic turbo, madwifi only), 11ast (A + static turbo, madwifi only),
            11fh (frequency hopping), 11lrs (LRS mode, broadcom only), 11ng (11N+11G, 2.4GHz,
            mac80211 only), 11na (11N+11A, 5GHz, mac80211 only) or auto.
            
            .. note:: AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param hwmode: the hardware mode to set for the device provided.
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

        """
        self.set_radio(dev, 'hwmode', hwmode, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_ht_capab(self, dev: int, ht_capab: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the available capabilities of the radio. The values are autodetected.
            This option is only used for type mac80211.
            
            .. note:: mac80211 is the default, we never change this.
                    AP default =  driver default
            
            :param dev: the wifi device index to set the region on
            :param ht_capab: specifies the ht_capab to set.
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'ht_capab', ht_capab, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_htmode(self, dev: int, htmode: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the channel width in 11ng and 11na mode, possible values are: HT20
            (single 20MHz channel), HT40- (2x 20MHz channels, primary/control channel is upper,
            secondary channel is below) or HT40+ (2x 20MHz channels, primary/control channel is
            lower, secondary channel is above. This option is only used for type mac80211.

            .. note:: mac80211 is the default, we never change this.
                    AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param htmode: the htmode to set
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'htmode', htmode, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_ieee80211w(self, dev:int, fpval: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Sets the management frame protection (802.11w) value

            ..note:: AP should be set for some wpa-psk encryptiopn setting in order for
                     ieee80211w to be set to some non-zero value.

            :param dev: the wifi device index to set the region on
            :param fpval: value to set for 802.11w, which has the following
                          meaning for openwrt: 2=required, 1=optional,
                          0=802.11w is disabled (same as ieee80211w setting being absent)
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'ieee80211w', fpval, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_isolate(self, dev: int, isolate: bool, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Isolate wireless clients from each other, only applicable in ap mode.
            Note: May not be supported in the original Backfire release for mac80211.

            :param dev: the wifi device index to set the region on
            :param isolate: A boolean indicating to isolate wireless clients
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'isolate', isolate, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_key(self, dev: int, key: Union[int, str], key_ordinal: Optional[int]=None, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
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
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        key_name = 'key'
        if key_ordinal is not None:
            key_name += str(key_ordinal)

        self.set_wifi_iface(dev, key_name, key, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_log_level(self, dev: int, log_level: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Set the log_level. Supported levels are:
                0 = verbose debugging
                1 = debugging,
                2 = informational messages
                3 = notification
                4 = warning

            :param dev: the wifi device index to set the region on
            :param log_level: The log level
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'log_level', log_level, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_macaddr(self, dev: int, macaddr: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Overrides the MAC address used for the wifi interface.

            :param dev: the wifi device index to set the region on
            :param macaddr: the mac address to use for an override address
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'macaddr', macaddr, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_macfilter(self, dev: int, macfilter: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the mac filter policy, disable to disable the filter, allow to
            treat it as whitelist or deny to treat it as blacklist.
            
            .. note:: Supported for the mac80211 since r25105
                    AP default = disable

            :param dev: the wifi device index to set the region on
            :param macfilter: (enable\disable)
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'macfilter', macfilter, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_maclist(self, dev: int, maclist: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Sets the list of MAC addresses to put into the mac filter.

            .. note:: Supported for the mac80211 since r25105

            :param dev: the wifi device index to set the region on
            :param maclist: List of space-separated mac addresses to allow/deny
                            according to wl0_macmode. Enter addresses with colons, e.g.:
                            "00:02:2D:08:E2:1D 00:03:3E:05:E1:1B" and put them in quotes if
                            you have more than one mac
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'maclist', maclist, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_max_listen_int(self, dev: int, max_listen_int: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Set the maximum allowed STA (client) listen interval. Association will be
            refused if a STA attempts to associate with a listen interval greater than
            this value. This option only has an effect on ap wifi-ifaces.
            
            .. note:: Only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param max_listen_int: the maximum allowed client listen interval
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'max_listen_int', max_listen_int, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_maxassoc(self, dev: int, maxassoc: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the maximum number of clients to connect.

            :param dev: the wifi device index to set the region on
            :param maxassoc: the max number of clients
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'maxassoc', maxassoc, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_mcast_rate(self, dev: int, mcast_rate: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Sets the fixed multicast rate, measured in kb/s.
            
            .. note:: Only supported by madwifi, and mac80211 (for type adhoc)

            :param dev: the wifi device index to set the region on
            :param mcast_rate: the fixed multicast rate in kb/s
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'mcast_rate', mcast_rate, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_mode(self, dev: int, mode: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Selects the operation mode of the wireless network, ap for Access Point, sta for
            managed (client) mode, adhoc for Ad-Hoc, wds for static WDS and monitor for monitor
            mode, mesh for 802.11s mesh mode.

            .. note:: mesh mode only supported by mac80211

            :param dev: the wifi device index to set the region on
            :param mode: the operation mode of the radio
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'mode', mode, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_network(self, dev: int, network: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the network interface to attach the wireless to.
            lan, wan, etc.

            :param dev: the wifi device index to set the region on
            :param network: the network interface
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'network', network, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_noscan(self, dev:int, noscan: bool, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Do not scan for overlapping BSSs in HT40+/- mode.
            
            .. note:: Only supported by mac80211 Turning this on will
                violate regulatory requirements!

            :param dev: the wifi device index to set the region on
            :param noscan: boolean indicating to not scan
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'noscan', noscan, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_radio(self, dev: int, parameter: str, value: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Set radio configuration option on OpenWrt AP.
            If no value is passed for a given param then the option is deleted.

            :param dev: device (0 or 1)
            :param parameter: parameter being configured
            :param value: - setting for parameter
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        prop_name = 'wireless.radio{}.{}'.format(dev, parameter)
        self.uci_set(prop_name, value, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_region(self, dev: int, country_code: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the wireless region to use. Region is specified using the 2-character country code.

            .. note::
                Region code modifications shall only be made on APs located in
                isolation chambers or screen rooms.

            :param dev: the wifi device index to set the region on
            :param country_code: two-character region code
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        if country_code not in REGION_CODES:
            raise ValueError("Invalid country code: {}".format(country_code))

        self.set_radio(dev, 'country', country_code, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_rxantenna(self, dev: int, rxantenna: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the antenna for receiving, the value may be driver specific,
            usually it is 1 for the first and 2 for the second antenna. Specifying 0
            enables automatic selection by the driver if supported. This option has
            no effect if diversity is enabled.

            .. note:: AP default = Driver default

            :param dev: the wifi device index to set the region on
            :param rxantenna: index of the receive antenna
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'rxantenna', rxantenna, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_ssid(self, dev: int, ssid: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            The broadcasted SSID of the wireless network (for managed mode the SSID of the network
            you're connecting to).

            :param dev: the wifi device index to set the region on
            :param ssid: the ssid to broadcast
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'ssid', ssid, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_txantenna(self, dev: int, txantenna: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the antenna for transmitting, values are identical to rxantenna.
            .. note:: AP default = Driver default

            :param dev: the wifi device index to set the region on
            :param txantenna: index of the receive antenna
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_radio(dev, 'txantenna', txantenna, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_txpower(self, dev: int, txpower: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the transmission power in dB.
            
            .. note:: AP default =  driver default

            :param dev: the wifi device index to set the region on
            :param txpower: the transmission power
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        return self.set_radio(dev, 'txpower', txpower, aspects=aspects, cmd_runner=cmd_runner)

    def set_wep_rekey(self, dev: int, wep_rekey: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the rekey interval in seconds.

            :param dev: the wifi device index to set the region on
            :param wep_rekey: rekey interval in seconds
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'wep_rekey', wep_rekey, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_wifi_iface(self, dev: int, parameter: str, value: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Set wireless interface configuration setting on OpenWrt AP
            If no value is passed for a given param then the option is deleted.

            :param dev: the wifi device index to set the region on
            :param parameter: parameter being configured
            :param value: setting for parameter
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        prop_name = 'wireless.@wifi-iface[{}].{}'.format(dev, parameter)
        rtnval = self.uci_set(prop_name, value, aspects=aspects, cmd_runner=cmd_runner)
        return rtnval

    def set_wmm(self, dev: int, enabled_state: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Enables/disables wmm support.

            :param dev: the wifi device index to set the region on
            :param enabled_state: 1 or 0 for enabled or disabled
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'wmm', enabled_state, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_wpa_group_rekey(self, dev: int, wpa_group_rekey: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param wpa_group_rekey: the wpa group rekey interval
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'wpa_group_rekey', wpa_group_rekey, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_wpa_pair_rekey(self, dev: int, wpa_pair_rekey: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Specifies the rekey interval in seconds

            :param dev: the wifi device index to set the region on
            :param wpa_pair_rekey: the wpa pair rekey interval
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'wpa_pair_rekey', wpa_pair_rekey, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_wps_device_name(self, dev: int, dev_name: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Sets the wps_devicename string

            :param dev: the wifi device index to set the region on
            :param dev_name: string to set for the WPS device name IE
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'wps_device_name', dev_name, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_wps_manufacturer(self, dev: int, manufacturer: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Gets the wps_manufacturer string

            :param dev: the wifi device index to set the region on
            :param manufacturer: string to set for the WPS manufacturer IE
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'wps_manufacturer', manufacturer, aspects=aspects, cmd_runner=cmd_runner)
        return

    def set_wps_pushbutton(self, dev: int, pbval: int, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Sets the wps_pushbutton config to be either 1 or 0

            :param dev: the wifi device index to set the region on
            :param pbval: value to set wps_pushbutton to
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        self.set_wifi_iface(dev, 'wps_pushbutton', pbval, aspects=aspects, cmd_runner=cmd_runner)
        return

    def uci_delete(self, prop_name: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Issues a 'uci delete' command to remove a configuration property

            :param prop_name: the router configuration property string
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        if aspects is None:
            aspects = self._aspects

        command = "uci delete {}".format(prop_name)
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
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

    def uci_get(self, prop_name: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None) -> str:
        """
            Issues the 'uci get' command to retrieve a value for a given property.
            Note: Converts integers and decimals to their respective primitives.

            :param prop_name: the router configuration property string
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.

            :returns: the value returned by uci
        """
        if aspects is None:
            aspects = self._aspects

        command = "uci get {}".format(prop_name)
        
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
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

    def uci_set(self, prop_name: str, prop_value: str, aspects: Optional[Aspects]=None, cmd_runner: Optional[ICommandRunner]=None):
        """
            Issues a 'uci set' command to change a configuration property

            .. note:: if the ' character is used in value it is automatically escaped
                    with the default UCI_ESCAPE_CHAR sequence for the AP

            :param prop_name: the router configuration property string
            :param prop_value: the value you wish to set param to or None if
                               you want to delete param
            :param aspects: The interop aspects to use when engaging with the router commandline interface
            :param cmd_runner: An optional ICommandRunner that is used to run commands.
        """
        if aspects is None:
            aspects = self._aspects

        command = "uci set {} {}".format(prop_name, prop_value)
        status, stdout, stderr = self._ssh_run_command(command, aspects=aspects, cmd_runner=cmd_runner)
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

    def _ssh_run_command(self, command: str, exp_status: Union[int, Sequence]=0, user: str = None,
                         pty_params: dict = None, aspects: Optional[Aspects] = None, cmd_runner: Optional[ICommandRunner]=None) -> Tuple[int, str, str]:
        """
            Private helper that will run a command on a remote machine via SSH.  If a ssh session object is
            open, then the session will be used to run the command, if a session is not open then the command
            is run via the normal ssh agent directly.
        """
        
        if aspects is None:
            aspects = self._aspects

        status, stdout, stderr = None, None, None

        if cmd_runner is not None:
            status, stdout, stderr = cmd_runner.run_cmd(command, exp_status=exp_status, user=user, pty_params=pty_params, aspects=aspects, cmd_runner=cmd_runner)
        else:
            status, stdout, stderr = self._ssh_agent.run_cmd(command, exp_status=exp_status, user=user, pty_params=pty_params, aspects=aspects, cmd_runner=cmd_runner)

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
