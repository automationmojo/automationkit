

import os
import socket

import zeroconf

class MdnsServiceInfo:
    def __init__(self, serviceinfo: zeroconf.ServiceInfo):
        self._serviceinfo = serviceinfo

    @property
    def addresses(self):
        return self._serviceinfo.addresses

    @property
    def first_ipv4_address(self):
        fipv4_addr = None

        for addr in self._serviceinfo.addresses:
            if len(addr) == 4: 
                fipv4_addr = socket.inet_ntoa(addr)
                break

        return fipv4_addr

    @property
    def host_ttl(self):
        return self._serviceinfo.host_ttl

    @property
    def interface_index(self):
        return self._serviceinfo.interface_index

    @property
    def key(self):
        return self._serviceinfo.key
    
    @property
    def other_ttl(self):
        return self._serviceinfo.other_ttl
    
    @property
    def port(self):
        return self._serviceinfo.port

    @property
    def priority(self):
        return self._serviceinfo.priority
    
    @property
    def properties(self):
        return self._serviceinfo.properties
    
    @property
    def server(self):
        return self._serviceinfo.server
    
    @property
    def server_key(self):
        return self._serviceinfo.server_key

    @property
    def svc_name(self):
        return self._serviceinfo.name
    
    @property
    def svc_type(self):
        return self._serviceinfo.type

    @property
    def text(self):
        return self._serviceinfo.text
    
    @property
    def weight(self):
        return self._serviceinfo.weight

    @property
    def wrapped_serviceinfo(self):
        return self._serviceinfo

    def detail_lines(self):

        str_lines = [
            "svc_name: {}".format(self.svc_name),
            "svc_type: {}".format(self.svc_type),
            "ipv4_addr: {}".format(self.first_ipv4_address),
            "svc_type: {}".format(self.svc_type),
            "properties"
        ]

        svc_props = self.properties

        svc_prop_keys = [k for k in svc_props]
        svc_prop_keys.sort()

        for key in svc_prop_keys:
            val = svc_props[key]
            if isinstance(val, bytes):
                str_lines.append("    {}: {}".format(key, repr(val.decode())))
            else:
                str_lines.append("    {}: {}".format(key, repr(val)))

        return str_lines

    def __str__(self):
        
        str_lines = self.detail_lines()
        strval = os.linesep.join(str_lines)

        return strval
