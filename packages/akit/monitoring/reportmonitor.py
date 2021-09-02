
import os

from akit.paths import get_path_for_artifacts
from akit.exceptions import AKitNotOverloadedError

DEFAULT_REPORT_INTERVAL = 10
class ReportMonitor:
    """
    """

    def __init__(self, report_class: str, report_topic: str, report_leaf: str, report_basename:str, interval: int=DEFAULT_REPORT_INTERVAL):
        self._report_class = report_class
        self._report_topic = report_topic
        self._report_leaf = report_leaf
        self._report_basename = report_basename
        self._report_dir = get_path_for_artifacts(report_leaf)
        self._report_file = os.path(self._report_dir, report_basename)
        self._report_to_ip = None
        self._report_to_port = None
        self._report_interval = interval
        return

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

    def finalize_report(self):
        errmsg = "The 'finalize_report' method must be overloaded by derived monitor types."
        raise AKitNotOverloadedError(errmsg)

    def process_report(self, ipaddr, rep_class, rep_content):
        errmsg = "The 'process_report' method must be overloaded by derived monitor types."
        raise AKitNotOverloadedError(errmsg)

    def set_report_endpoint(self, ipaddr, port):
        self._report_to_ip = ipaddr
        self._report_to_port = port
        return
