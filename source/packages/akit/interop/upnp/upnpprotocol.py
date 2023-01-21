"""
.. module:: upnpprotocols
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`MSearchRootDeviceProtocol` class and
               associated diagnostic.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Optional, Tuple

import copy
import os
import re
import socket
import threading

import netifaces

from akit.exceptions import AKitTimeoutError

from akit.xlogging.foundations import getAutomatonKitLogger

from akit.networking.multicast import create_multicast_socket_for_iface, create_multicast_socket
from akit.networking.unicast import create_unicast_socket
from akit.networking.interfaces import get_interface_for_ip

from akit.waiting import ProgressOfDurationWaitContext, WaitContext

REGEX_NOTIFY_HEADER = re.compile("NOTIFY[ ]+[*/]+[ ]+HTTP/1")

logger = getAutomatonKitLogger()

class MSearchTargets:
    """
        MSearch target constants.
    """
    ROOTDEVICE = "upnp:rootdevice"
    ALL="ssdp:all"

class MSearchKeys:
    """
        MSearch dictionary or header keys that MSearch response data items are stored under.
    """
    CACHE_CONTROL = "CACHE-CONTROL"
    EXT = "EXT"
    LOCATION = "LOCATION"
    NTS = "NTS"
    SERVER = "SERVER"
    ST = "ST"
    USN = "USN"
    USN_DEV = "USN_DEV"
    USN_CLS = "USN_CLS"

    IP = "IP"
    ROUTES = "ROUTES"

class MSearchRouteKeys:
    """
        The dictionary keys that MSearch interface routing information is stored under.
    """
    IFNAME = "LOCAL_IFNAME"
    IP = "LOCAL_IP"

class UpnpProtocol:
    """
        UPnP Protocol constants.
    """
    MULTICAST_ADDRESS = '239.255.255.250'
    PORT = 1900

    HEADERS = {
        "ST": MSearchTargets.ROOTDEVICE,
        "Man": "ssdp:discover",
        "MX": "1"
    }

SSDP_IPV6_MULTICAST_ADDRESS_LINK_LOCAL="FF02::C"
SSDP_IPV6_MULTICAST_ADDRESS_SITE_LOCAL="FF05::C"
SSDP_IPV6_MULTICAST_ADDRESS_ORG_LOCAL="FF08::C"
SSDP_IPV6_MULTICAST_ADDRESS_GLOBAL_LOCAL="FF0E::"

class MSearchScanContext:
    """
        The :class:`MSearchScanContext` is an object that allows the sharing of scan results across threads
        that are scanning mulitple interfaces.  We utilize a shared scan context so we can find the devices
        faster.
    """

    def __init__(self, upnp_device_hints):
        self.upnp_device_hints = upnp_device_hints
        self.remaining_device_hints = [dh for dh in upnp_device_hints]

        self.have_hints = False
        if len(self.remaining_device_hints) > 0:
            self.have_hints = True

        self.continue_scan = True

        self.found_devices = {}
        self.matching_devices = {}

        self.lock = threading.Lock()
        return

    def register_device(self, ifname: str, usn: str, device_info: dict, route_info: dict):
        """
            Method called by msearch scan threads to register msearch results for a specific network interface.

            :param ifname: The interface name to register msearch results for.
            :param usn: The UPNP usn to register msearch results for.
            :param device_info: A dictionary containing the information about the device found by the msearch thread.
            :param route_info: The route info about the interface that the device was found on.
        """
        # pylint: disable=unused-argument
        self.lock.acquire()
        try:
            if usn not in self.found_devices:

                device_info[MSearchKeys.ROUTES] = {ifname: route_info}

                self.found_devices[usn] = device_info

                for hint in self.remaining_device_hints:
                    if usn.find(hint) > -1:
                        self.remaining_device_hints.remove(hint)
                        self.matching_devices[hint] = device_info
                        break

                if self.have_hints and len(self.remaining_device_hints) == 0:
                    self.continue_scan = False
            else:
                existing_info = self.found_devices[usn]

                if MSearchKeys.ROUTES not in existing_info:
                    existing_info[MSearchKeys.ROUTES] = {ifname: route_info}
                else:
                    existing_info[MSearchKeys.ROUTES].update({ifname: route_info})

        finally:
            self.lock.release()

        return

def msearch_parse_request(content: bytes) -> dict:
    """
        Takes in the content of the MSEARCH request and parses it into a
        python dictionary object.

        :param content: MSearch request content as a bytes.

        :return: A python dictionary with key and values from the MSearch request
    """
    content = content.decode('utf-8')

    respinfo = None

    resplines = content.splitlines(False)
    if len(resplines) > 0:
        header = resplines.pop(0).strip()
        if header.startswith("M-SEARCH *"):
            respinfo = {}
            for nxtline in resplines:
                cidx = nxtline.find(":")
                if cidx > -1:
                    key = nxtline[:cidx].upper()
                    val = nxtline[cidx+1:].strip()
                    respinfo[key] = val

    return respinfo

def msearch_parse_response(content: bytes) -> dict:
    """
        Takes in the content of the response of an MSEARCH request and parses it into a
        python dictionary object.

        :param content: MSearch response content as a bytes.

        :return: A python dictionary with key and values from the MSearch response
    """
    content = content.decode('utf-8')

    respinfo = None

    resplines = content.splitlines(False)
    if len(resplines) > 0:
        header = resplines.pop(0).strip()
        if header.startswith("HTTP/"):
            respinfo = {}
            for nxtline in resplines:
                cidx = nxtline.find(":")
                if cidx > -1:
                    key = nxtline[:cidx].upper()
                    val = nxtline[cidx+1:].strip()
                    respinfo[key] = val

    return respinfo


def msearch_query_host(target_address: str, query_usn: Optional[str]=None, mx: int = 5, st: str = MSearchTargets.ROOTDEVICE,
                response_timeout: float = 45, ttl: int = 1, unicast_socket: bool=False, custom_headers: Optional[dict]=None,
                wctx: Optional[WaitContext]=None):
    """
        The inline msearch function provides a mechanism to do a synchronous msearch
        in order to determine if a specific host  devices is available and to
        determine the interface that the device is available on.

        :param target_address: The network address of the device being targeted by the unicast mquery
        :param query_usn: The USN of the device that is being queried
        :param mx:  Instructs the M-SEARCH targets to wait a random time from 0-mx before sending a response.
        :param st: The search target of the MSearch.
        :param response_timeout:  The timeout to wait for responses from all the expected devices.
        :param ttl: The time to live for the multicast packet
                    0 = same host
                    1 = same subnet
                    32 = same site
                    64 = same region
                    128 = same continent
                    255 = unrestricted scope
        :param unicast_socket: Utilize a unicast socket configuration for the query, else use a multicast socket configuration
        :param custom_headers: Custom headers that are added to the query message.

        :raises: TimeoutError, KeyboardInterrupt
    """

    found_device_info = None

    target_address = target_address.encode()

    msearch_msg_lines = [
        b'M-SEARCH * HTTP/1.1',
        b'HOST: %s:%d' % (UpnpProtocol.MULTICAST_ADDRESS.encode("utf-8"), UpnpProtocol.PORT),
        b'MAN: "ssdp:discover"',
        b'ST: %s' % st.encode("utf-8")
    ]

    if custom_headers is not None:
        for hname, hval in custom_headers.items():
            hname = hname.upper().encode("utf-8")
            msearch_msg_lines.append(b'%s: %s' % (hname, hval.encode("utf-8")))

    msearch_msg_lines.append(b'')

    msearch_msg = b"\r\n".join(msearch_msg_lines)

    sock = None

    if unicast_socket:
        sock = create_unicast_socket(target_address, UpnpProtocol.PORT, socket.AF_INET, ttl=ttl, timeout=response_timeout)
    else:
        sock = create_multicast_socket(UpnpProtocol.MULTICAST_ADDRESS, UpnpProtocol.PORT, socket.AF_INET, ttl=ttl, timeout=response_timeout)
                
    if wctx is None:
        wctx = WaitContext(response_timeout)

    wctx.mark_begin()

    try:
        sock.sendto(msearch_msg, (target_address, UpnpProtocol.PORT))

        while True:
     
            try:
                resp, addr = sock.recvfrom(1024)

                if addr == target_address:
                    if resp.startswith(b"NOTIFY * HTTP/"):
                        resp = resp.lstrip(b"NOTIFY * ")

                    if resp.startswith(b"HTTP/"):
                        device_info = msearch_parse_response(resp)
                        if device_info is not None:
                            foundst = device_info.get(MSearchKeys.NTS, None)
                            if foundst == 'ssdp:alive':
                                if MSearchKeys.USN in device_info:
                                    usn_dev= device_info[MSearchKeys.USN]
                                    usn_dev = usn_dev.lstrip("uuid:")
                                    
                                    device_info[MSearchKeys.USN_DEV] = usn_dev

                                    if query_usn is None or usn_dev == query_usn:

                                        ip_addr = addr[0]
                                        ifname = get_interface_for_ip(ip_addr)

                                        route_info = {
                                            MSearchRouteKeys.IFNAME: ifname,
                                            MSearchRouteKeys.IP: ip_addr
                                        }
                                        device_info[MSearchKeys.ROUTES] = {ifname: route_info}
                                        device_info[MSearchKeys.IP] = ip_addr

                                        found_device_info = device_info

                                else:
                                    print("device_info didn't have a USN. %r" % device_info)
                        else:
                            print("device_info was None.")
                else:
                    print("Respons from other addr={}".format(addr))

            except socket.timeout as toerr:
                pass
            
            if not wctx.should_continue() and wctx.has_timed_out:
                wctx.mark_timeout()
                break
    except Exception:
        logger.exception("msearch_query_host exception:")
    except KeyboardInterrupt: # pylint: disable=try-except-raise
        raise
    finally:
        sock.close()

    return found_device_info


def msearch_on_interface(scan_context: MSearchScanContext, ifname: str, ifaddress: str, *,
                         mx: int = 5, st: str = MSearchTargets.ROOTDEVICE, response_timeout: float = 45,
                         ttl: int = 1, custom_headers: Optional[dict]=None, wctx: Optional[WaitContext]=None):
    """
        The inline msearch function provides a mechanism to do a synchronous msearch
        in order to determine if a set of available devices are available and to
        determine the interfaces that each device is listening on.

        :param scan_context: A shared scan context that shares information between the scan threads and
                             speeds up the process of finding the expected UPNP devices across the
                             interfaces.
        :param ifname: The name if the interface being searched.
        :param ifaddress: The IP address of the interface being searched.
        :param mx:  Instructs the M-SEARCH targets to wait a random time from 0-mx before sending a response.
        :param st: The search target of the MSearch.
        :param response_timeout:  The timeout to wait for responses from all the expected devices.
        :param interval: The retry interval to wait before retrying to search for an expected device.
        :param ttl: The time to live for the multicast packet
                    0 = same host
                    1 = same subnet
                    32 = same site
                    64 = same region
                    128 = same continent
                    255 = unrestricted scope
        :param custom_headers: Optional custom msearch headers.
        :param wctx: An option wait context to use for waiting

        :returns:  dict -- A dictionary of the devices that were found.
        :raises: TimeoutError, KeyboardInterrupt
    """

    route_info = {
        MSearchRouteKeys.IFNAME: ifname,
        MSearchRouteKeys.IP: ifaddress
    }

    multicast_address = UpnpProtocol.MULTICAST_ADDRESS
    multicast_port = UpnpProtocol.PORT

    msearch_msg_lines = [
        b'M-SEARCH * HTTP/1.1',
        b'HOST: %s:%d' % (UpnpProtocol.MULTICAST_ADDRESS.encode("utf-8"), UpnpProtocol.PORT),
        b'MAN: "ssdp:discover"',
        b'ST: %s' % st.encode("utf-8")
    ]

    if custom_headers is not None:
        for hname, hval in custom_headers.items():
            hname = hname.upper().encode("utf-8")
            msearch_msg_lines.append(b'%s: %s' % (hname, hval.encode("utf-8")))

    msearch_msg_lines.append(b'')

    msearch_msg = b"\r\n".join(msearch_msg_lines)

    sock = None

    try:
        sock = create_multicast_socket_for_iface(UpnpProtocol.MULTICAST_ADDRESS, ifname, UpnpProtocol.PORT, socket.AF_INET, ttl=ttl, timeout=5)

        sock.sendto(msearch_msg, (multicast_address, multicast_port))

        if wctx is None:
            wctx = WaitContext(response_timeout)

        wctx.mark_begin()

        while True:

            try:
                resp, addr = sock.recvfrom(1024)
                if resp.startswith(b"NOTIFY * HTTP/"):
                    resp = resp.lstrip(b"NOTIFY * ")

                if resp.startswith(b"HTTP/"):
                    device_info = msearch_parse_response(resp)

                    if device_info is not None:
                        foundst = device_info.get(MSearchKeys.ST, None)
                        if foundst == st:
                            if MSearchKeys.USN in device_info:
                                usn_dev, usn_cls = device_info[MSearchKeys.USN].split("::")
                                usn_dev = usn_dev.lstrip("uuid:")
                                if usn_cls == "upnp:rootdevice":
                                    device_info[MSearchKeys.USN_DEV] = usn_dev
                                    device_info[MSearchKeys.USN_CLS] = usn_cls

                                    device_info[MSearchKeys.IP] = addr[0]

                                    scan_context.register_device(ifname, usn_dev, device_info, route_info)
                            else:
                                print("device_info didn't have a USN. %r" % device_info)
                    else:
                        print("device_info was None.")

            except socket.timeout:
                pass

            if not wctx.should_continue() and wctx.has_timed_out:
                wctx.mark_timeout()
                break

            if not scan_context.continue_scan:
                break
    except Exception:
        logger.exception("msearch_on_interface exception:")
    except KeyboardInterrupt: # pylint: disable=try-except-raise
        raise
    finally:
        sock.close()

    return


def msearch_scan(expected_devices, interface_list=None, response_timeout=45, interval=2, raise_exception=False,
                 custom_headers: Optional[dict]=None, show_progress=False) -> Tuple[dict, dict]:
    """
        Performs a msearch across a list of interfaces for a specific expected device.  This method is typically used
        during a persistent search when a device was not found in a broad msearch.

        :param expected_devices: A list of USN(s) of a list of devices to search for.
        :param interface_list: A list of interface names to scan for the device.
        :param response_timeout:  The timeout to wait for responses from all the expected devices.
        :param interval: The retry interval to wait before retrying to search for an expected device.
        :param raise_exception: A boolean indicating if the mquery should raise an exception on failure.
        :param custom_headers: Custom headers to include in the msearch message
        :param show_progress: Should progress be rendered to the console.

        :returns: A tuple with a dictionary of found and a dictionary of matching devices found.
    """
    if interface_list is None:
        interface_list = netifaces.interfaces()

    scan_context = MSearchScanContext(expected_devices)

    search_threads = []

    progress = None
    if show_progress:
        progress = ProgressOfDurationWaitContext.create_rich_progress()

    try:
        if progress is not None:
            progress.start()

        for ifname in interface_list:
            ifaddress = None

            address_info = netifaces.ifaddresses(ifname)
            if address_info is not None:
                # First look for IPv4 address information
                if netifaces.AF_INET in address_info:
                    addr_info = address_info[netifaces.AF_INET][0]
                    ifaddress = addr_info["addr"]

                # If we didn't find an ipv4 address, try using IPv6
                # if ifaddress is None and netifaces.AF_INET6 in addr_info:
                #    addr_info = address_info[netifaces.AF_INET6][0]
                #    ifaddress = addr_info["addr"]

                if ifaddress is not None:
                    thname = "msearch-%s" % ifname
                    thargs = (scan_context, ifname, ifaddress)
                    wctx = None
                    if progress is not None:
                        wctx = ProgressOfDurationWaitContext(progress, thname, timeout=response_timeout)
                    else:
                        wctx = WaitContext(timeout=response_timeout)

                    thkwargs = { "wctx": wctx, "custom_headers": custom_headers}

                    sthread = threading.Thread(name=thname, target=msearch_on_interface, args=thargs, kwargs=thkwargs)
                    sthread.start()
                    search_threads.append(sthread)

        # Wait for all the search threads to finish
        while len(search_threads) > 0:
            nxt_thread = search_threads.pop(0)
            nxt_thread.join()

    finally:
        if progress is not None:
            progress.stop()

    found_devices = copy.deepcopy(scan_context.found_devices)
    matching_devices = copy.deepcopy(scan_context.matching_devices)

    if raise_exception and len(matching_devices) != len(expected_devices):
        err_msg = "Failed to find expected UPNP devices after a timeout of %s seconds.\n" % response_timeout

        missing = [dkey for dkey in expected_devices]
        for dkey in scan_context.found_devices:
            if dkey in missing:
                missing.remove(dkey)

        err_msg_lines = []
        err_msg_lines.append("EXPECTED: (%s)" % len(expected_devices))
        for dkey in expected_devices:
            err_msg_lines.append("    %r:" % dkey)
        err_msg_lines.append("")

        err_msg_lines.append("MATCHING: (%s)" % len(matching_devices))
        for dkey in matching_devices:
            err_msg_lines.append("    %r:" % dkey)
        err_msg_lines.append("")

        err_msg_lines.append("FOUND: (%s)" % len(found_devices))
        for dkey in found_devices:
            err_msg_lines.append("    %r:" % dkey)
        err_msg_lines.append("")

        err_msg_lines.append("MISSING: (%s)" % len(missing))
        for dkey in missing:
            err_msg_lines.append("    %r:" % dkey)
        err_msg_lines.append("")

        err_msg = os.linesep.join(err_msg_lines)
        raise AKitTimeoutError(err_msg) from None

    return found_devices, matching_devices

def notify_parse_request(content: str) -> dict:
    """
        Takes in the content of the NOTIFY request and parses it into a
        python dictionary object.

        :param content: Notify request content as a string.

        :return: A python dictionary with key and values from the Notify request
    """
    content = content.decode('utf-8')

    resp_headers = None
    resp_body = None

    mobj = REGEX_NOTIFY_HEADER.search(content)
    if mobj is not None:
        header_content = None
        body_content = None

        if content.find("\r\n\r\n") > -1:
            header_content, body_content = content.split("\r\n\r\n", 1)
        elif content.find("\n\n") > -1:
            header_content, body_content = content.split("\n\n", 1)
        else:
            header_content = content

        resplines = header_content.splitlines(False)

        # Pop the NOTIFY header
        resplines.pop(0).strip()

        resp_headers = {}
        for nxtline in resplines:
            cidx = nxtline.find(":")
            if cidx > -1:
                key = nxtline[:cidx].upper()
                val = nxtline[cidx+1:].strip()
                resp_headers[key] = val

        if body_content is not None:
            resp_body = body_content

    return resp_headers, resp_body
