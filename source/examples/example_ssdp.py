import asyncio
import socket
import ssdp

st = "upnp:rootdevice"

MSEARCH_ = [
    'M-SEARCH * HTTP/1.1',
    'Host:239.255.255.250:1900',
    'ST:%s' % (st,),
    'Man:"ssdp:discover"',
    'MX:1',
    '']

class MSearchTargets:
    ROOTDEVICE = "upnp:rootdevice"
    ALL="ssdp:all"

class MSearchScanner(ssdp.SimpleServiceDiscoveryProtocol):

    PORT = 1900
    HEADERS = {
        "ST": MSearchTargets.ALL,
        "Man": "ssdp:discover",
        "MX": "1"
    }

    def response_received(self, response, addr):
        print(response, addr)
        print()

    def request_received(self, request, addr):
        print(request, addr)
        print()

print()
print()
print("=============================================================================================")
print()
print()

loop = asyncio.get_event_loop()
connect = loop.create_datagram_endpoint(MSearchScanner, family=socket.AF_INET)
transport, protocol = loop.run_until_complete(connect)

notify = ssdp.SSDPRequest('M-SEARCH', headers=MSearchScanner.HEADERS)
notify.sendto(transport, (MSearchScanner.MULTICAST_ADDRESS, MSearchScanner.PORT))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()