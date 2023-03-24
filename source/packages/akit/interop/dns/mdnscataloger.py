

import threading
import time

from akit.networking.multicast import create_multicast_socket
from akit.networking.constants import MDNS_GROUP_ADDR, MDNS_GROUP_ADDR6, MDNS_PORT

from akit.interop.dns.dnsinboundmessage import DnsInboundMessage
from akit.interop.dns.dnsoutboundmessage import DnsOutboundMessage
from akit.interop.dns.dnsquestion import DnsQuestion
from akit.interop.dns.dnsconst import DnsRecordType, DnsRecordClass

class MdnsCataloger:

    def __init__(self):
        self._listener = None
        self._listening = False
        self._listen_sock = None
        self._lock = threading.RLock()
        return
    
    def pose_question(self, question: DnsQuestion):
        return

    def query_service(self, svc_name):
        
        question = DnsQuestion(svc_name, DnsRecordType.PTR, DnsRecordClass.IN)

        packet = DnsOutboundMessage()

        return

    def start(self):

        sgate = threading.Event()
        sgate.clear()

        self._listening = True
        self._listener = threading.Thread(target=self._thread_entry_monitor, name="mdns-cataloger", args=(sgate,))
        self._listener.daemon = True
        self._listener.start()
        sgate.wait()

        return

    def _thread_entry_monitor(self, sgate: threading.Event):

        sgate.set()

        while(self._listening):

            try:
                self._lock.acquire()
                try:
                    self._listen_sock = create_multicast_socket(MDNS_GROUP_ADDR, MDNS_PORT)
                finally:
                    self._lock.release()

                while(self._listening):
                    try:
                        request, addr = None, None

                        self._lock.acquire()
                        try:
                            request, addr = self._listen_sock.recvfrom(2048)
                        finally:
                            self._lock.release()

                        packet = DnsInboundMessage(request)

                        if packet.is_query():
                            print (packet)
                        elif packet.is_response():
                            print (packet)
                        else:
                            print(f"Unknown package type received from {addr}")

                    except Exception as xcpt:
                        pass
            
            finally:
                self._lock.acquire()
                try:
                    self._listen_sock.close()
                finally:
                    self._lock.release()

        return
    
if __name__ == "__main__":

    cataloger = MdnsCataloger()
    cataloger.start()

    while True:
        time.sleep(2)
        print("tick")
        time.sleep(2)
        print("tock")