from typing import List

from akit.interop.dns.dnsconst import DnsRecordClass, DnsRecordType

from akit.interop.dns.dnsquestion import DnsQuestion

from akit.interop.dns.dnsserver import DnsServer

def dns_query_name(name: str, rtype: DnsRecordType, rclass: DnsRecordClass):

    question = DnsQuestion(name, rtype, rclass)

    query_str = question.as_dns_string()

    return query_str

def dns_query_services(service_types: List[str], rtype: DnsRecordType=DnsRecordType.PTR, rclass: DnsRecordClass=DnsRecordClass.IN):
    
    service = DnsServer()
    
    service.start()

    service.wait()

    return

if __name__ == "__main__":
    from akit. interop.dns.dnsconst import DnsKnownServiceTypes

    server = dns_query_services([DnsKnownServiceTypes.SONOS])