
import socket
import threading
from akit.exceptions import AKitSemanticError

from akit.xthreading.looper import Looper
from akit.xthreading.looperpool import LooperPool
from akit.monitoring.reportmonitor import ReportMonitor
from akit.networking.interfaces import get_correspondance_ip_address


REPORT_HEADER_LENGTH = 7

class ReportingServiceLooper(Looper):
    """
    """

    def loop(self, packet) -> bool: # pylint: disable=no-self-use
        """
            Method that is overloaded by derived classes in order to implement a work loop.
        """
        service, ipaddr, rep_class, rep_topic, rep_content = packet

        monitor = service.lookup_monitor(rep_class, rep_topic)
        if monitor is not None:
            monitor.process_report(ipaddr, rep_content)

        return True


class ReportingService:
    """
    """

    def __init__(self, highwater: int=5, daemon=True):
        self._looper_pool = LooperPool(ReportingServiceLooper, min_loopers=1,
                                       max_loopers=1, highwater=highwater, daemon=daemon)

        self._daemon = daemon
        self._service_thread = None

        self._monitor_table = {}
        self._running = False

        self._port = 0
        self._svc_sock = None

        self._lock = threading.RLock()
        return

    def lookup_monitor(self, monitor_class: str, monitor_topic: str) -> ReportMonitor:

        monitor_name = "{}:{}".format(monitor_class, monitor_topic)

        monitor = None

        self._lock.acquire()
        try:
            if monitor_name in self._monitor_table:
                monitor = self._monitor_table[monitor_name]
        finally:
            self._lock.release()

        return monitor

    def register_monitor(self, monitor: ReportMonitor):
        """
        """
        monitor_name = "{}:{}".format(monitor.report_class, monitor.report_topic)

        self._lock.acquire()
        try:
            if monitor_name in self._monitor_table:
                errmsg = "A 'ReportMonitor' named '{}' has already been registered.".format(monitor_name)
                raise AKitSemanticError(errmsg) from None

            self._monitor_table[monitor_name] = monitor

            corr_ip = monitor.correspondance_ip
            monitor.set_report_endpoint(corr_ip, self._port)
        finally:
            self._lock.release()

        return

    def start(self):

        self._lock.acquire()
        try:
            sgate = threading.Event()
            sgate.clear()

            self._service_thread = threading.Thread(name="Accept", 
                target=self._service_thread_entry, args=(sgate,))
            self._service_thread.daemon = self._daemon
            self._service_thread.start()

            self._lock.release()
            try:
                sgate.wait()
            finally:
                self._lock.acquire()
        finally:
            self._lock.release()

        self._looper_pool.start_pool()

        return

    def _service_thread_entry(self, sgate):

        self._lock.acquire()
        try:
            self._running = True

            try:
                self._svc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Bind to all interfaces and also bint to port zero so we can get
                # an ephimeral port address
                self._svc_sock.bind(("0.0.0.0", 0))

                # We dont keep track of host because we need to provide a host address
                # that is relative to the device and the interface we can communicate
                # with a device on.
                _, self._port = self._svc_sock.getsockname()

                self._svc_sock.listen(1)

                sgate.set()
                sgate = None

                self._lock.release()
                try:

                    while self._running:
                        asock, claddr = self._svc_sock.accept()

                        try:
                            header = asock.recv(REPORT_HEADER_LENGTH)
                            msg_size = int(header.rstrip(b":"))

                            msg_body = asock.recv(msg_size)
                            msg_body = msg_body.decode()

                            rep_cls_end = msg_body.find(":")
                            rep_topic_end = msg_body.find(":", rep_cls_end + 1)
                            if rep_cls_end > -1 and rep_topic_end > -1:
                                rep_class = msg_body[:rep_cls_end]
                                rep_topic = msg_body[rep_cls_end + 1: rep_topic_end]
                                rep_content = msg_body[rep_topic_end + 1:]

                                wkpacket = (self, claddr, rep_class, rep_topic, rep_content)
                                self._looper_pool.push_work(wkpacket)

                        except:
                            import traceback
                            errmsg = traceback.format_exc()
                            print(errmsg)
                        finally:
                            asock.close()

                finally:
                    self._lock.acquire()

            finally:
                if self._svc_sock is not None:
                    self._svc_sock.close()

                if sgate is not None:
                    sgate.set()
        finally:
            self._lock.release()

        return
