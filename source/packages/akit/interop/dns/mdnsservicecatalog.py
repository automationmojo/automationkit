
from typing import Dict, List, Optional

import os
import threading

import zeroconf

from akit.xlogging.foundations import AKitLoggerWrapper, AKitLogLevels

from akit.interop.dns.mdnsserviceinfo import MdnsServiceInfo
from akit.waiting import WaitContext

class MdnsServiceCatalog(zeroconf.ServiceListener):
    """
    """

    def __init__(self, logger: Optional[AKitLoggerWrapper]=None, log_level: AKitLogLevels=AKitLogLevels.INFO):
        self._logger = logger
        self._log_level = log_level
        
        self._lock = threading.Lock()
        self._service_catalog: Dict[str, Dict[str, zeroconf.ServiceInfo]] = {}
        return

    def update_service(self, zc: zeroconf.Zeroconf, svc_type: str, svc_name: str) -> None:

        svc_info = MdnsServiceInfo(zc.get_service_info(svc_type, svc_name))
        
        self._lock.acquire()
        try:
            svc_name_catalog = self._pull_svcname_catalog_for_svctype(svc_type)
            svc_name_catalog[svc_name] = svc_info
        finally:
            self._lock.release()

        self._log_service_activity(svc_type, svc_name, svc_info, "Service update type={} name={}.")

        return
    
    def remove_service(self, zc: zeroconf.Zeroconf, svc_type: str, svc_name: str) -> None:

        svc_info = None

        self._lock.acquire()
        try:
            svc_name_catalog = self._pull_svcname_catalog_for_svctype(svc_type)
            svc_info = svc_name_catalog[svc_name]
            del svc_name_catalog[svc_name]
        finally:
            self._lock.release()

        self._log_service_activity(svc_type, svc_name, svc_info, "Service remove type={} name={}.")

        return

    def add_service(self, zc: zeroconf.Zeroconf, svc_type: str, svc_name: str) -> None:
        
        svc_info = MdnsServiceInfo(zc.get_service_info(svc_type, svc_name))
    
        self._lock.acquire()
        try:
            svc_name_catalog = self._pull_svcname_catalog_for_svctype(svc_type)
            svc_name_catalog[svc_name] = svc_info
        finally:
            self._lock.release()

        self._log_service_activity(svc_type, svc_name, svc_info, "Service add type={} name={}.")

        return

    def list_service_names_for_type(self, svc_type: str) -> List[str]:

        svc_name_list = None
        
        self._lock.acquire()
        try:
            svc_name_catalog = self._pull_svcname_catalog_for_svctype(svc_type)
            svc_name_list = [ svc_name for svc_name in svc_name_catalog.keys()]
        finally:
            self._lock.release()
    
        svc_name_list.sort()

        return svc_name_list

    def lookup_service_catalog_for_type(self, svc_type: str) -> MdnsServiceInfo:
        
        svc_name_catalog = {}

        self._lock.acquire()
        try:
            # Create a copy of the service catalog to return so we don't create a issue
            # with multiple thread sharing a dict collection type
            svc_name_catalog.update(self._pull_svcname_catalog_for_svctype(svc_type))
        finally:
            self._lock.release()

        return svc_name_catalog

    def lookup_service_info(self, svc_type: str, svc_name: str) -> MdnsServiceInfo:
        
        service_info = None

        self._lock.acquire()
        try:
            svc_name_catalog = self._pull_svcname_catalog_for_svctype(svc_type)

            if svc_name in svc_name_catalog:
                service_info = svc_name_catalog[svc_name]
        finally:
            self._lock.release()

        return service_info

    def wait_for_services_in_service_catalog(self, wctx: WaitContext, zc: zeroconf.Zeroconf, svc_type: str, svc_query_names: List[str], exact_match=False):

        all_present = True

        if wctx.is_do_every_interval:
            # If this is a do every interval, send out another copy of our DNSQuestion
            out = zeroconf.DNSOutgoing(zeroconf.const._FLAGS_QR_QUERY, multicast=True)
            question = zeroconf.DNSQuestion(svc_type, zeroconf.const._TYPE_PTR, zeroconf.const._CLASS_IN)
            out.add_question(question)
            zc.send(out)
            
        service_catalog = self.lookup_service_catalog_for_type(svc_type)

        if exact_match:
            for exp_svc_name in svc_query_names:

                item_found = False
                for svc_name in service_catalog:
                    if svc_name == exp_svc_name:
                        item_found = True
                        break

                if not item_found:
                    all_present = False
                    break
        else:
            for exp_svc_name in svc_query_names:

                item_found = False
                for svc_name in service_catalog:
                    if svc_name.startswith(exp_svc_name):
                        item_found = True
                        break

                if not item_found:
                    all_present = False
                    break

        if not all_present and wctx.final_attempt:
            what_for = "Timeout waiting for sevice discovery for mdns services:"

            detail_lines = [
                "SERVICE NAMES:"
            ]
            for sqname in svc_query_names:
                detail_lines.append(f"    {sqname}")

            toerr = wctx.create_timeout(what_for, detail_lines)
            raise toerr

        return all_present

    def _log_service_activity(self, svc_type: str, svc_name: str, svc_info: MdnsServiceInfo, what_template: str):

        msg_lines = [
            what_template.format(svc_type, svc_name)
        ]

        if self._log_level <= AKitLogLevels.DEBUG:
            msg_lines.extend(svc_info.detail_lines())
            msg_lines.append("")

        msg = os.linesep.join(msg_lines)

        if self._logger is not None:
            self._logger.info(msg)
        else:
            print(msg)

        return

    def _pull_svcname_catalog_for_svctype(self, svc_type: str) -> Dict[str, MdnsServiceInfo]:

        svc_name_catalog = None
        if svc_type not in self._service_catalog:
            svc_name_catalog = {}
            self._service_catalog[svc_type] = svc_name_catalog
        else:
            svc_name_catalog = self._service_catalog[svc_type]
        
        return svc_name_catalog
