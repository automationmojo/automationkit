
import os

from akit.paths import get_path_for_artifacts
from akit.exceptions import AKitNotOverloadedError
from akit.networking.interfaces import get_correspondance_ip_address

DEFAULT_REPORT_INTERVAL = 10
class ReportMonitor:
    """
    """

    def __init__(self, reporting_ip: str, report_class: str, report_topic: str, report_leaf: str, report_basename:str,
                 interval: int=DEFAULT_REPORT_INTERVAL, correspondance_ip: str=None, chk_port: int=80):
        self._reporting_ip = reporting_ip
        self._report_class = report_class
        self._report_topic = "{}/{}".format(reporting_ip, report_topic)
        self._report_leaf = report_leaf
        self._report_basename = report_basename
        self._report_dir = get_path_for_artifacts(report_leaf)
        self._report_file = os.path.join(self._report_dir, report_basename)
        self._report_to_ip = None
        self._report_to_port = None
        self._report_interval = interval

        self._correspondance_ip = correspondance_ip
        if correspondance_ip is None:
            self._correspondance_ip = get_correspondance_ip_address(self._reporting_ip, chk_port)
        return

    @property
    def correspondance_ip(self):
        return self._correspondance_ip

    @property
    def report_basename(self):
        return self._report_basename

    @property
    def report_class(self):
        return self._report_class

    @property
    def report_dir(self):
        return self._report_dir

    @property
    def report_file(self):
        return self._report_file

    @property
    def report_interval(self):
        return self._report_interval

    @property
    def report_leaf(self):
        return self._report_leaf

    @property
    def report_topic(self):
        return self._report_topic

    @property
    def reporting_ip(self):
        return self._reporting_ip

    def finalize_report(self):
        errmsg = "The 'finalize_report' method must be overloaded by derived monitor types."
        raise AKitNotOverloadedError(errmsg) from None

    def process_report(self, ipaddr, rep_class, rep_content):
        errmsg = "The 'process_report' method must be overloaded by derived monitor types."
        raise AKitNotOverloadedError(errmsg) from None

    def set_report_endpoint(self, ipaddr, port):
        self._report_to_ip = ipaddr
        self._report_to_port = port
        return
