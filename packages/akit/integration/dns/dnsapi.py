from typing import List

from akit.integration.dns.dnsconst import DnsRecordClass, DnsRecordType

from akit.integration.dns.dnsquestion import DnsQuestion

def dns_query_name(name: str, rtype: DnsRecordType, rclass: DnsRecordClass):

    question = DnsQuestion(name, rtype, rclass)

    query_str = question.as_dns_string()

    return query_str

def dns_query_services(service_types: List[str], rtype: DnsRecordType=DnsRecordType.PTR, rclass: DnsRecordClass=DnsRecordClass.IN):
    
    for svc in service_types:
        question = DnsQuestion(svc, rtype, rclass)

        

    return

if __name__ == "__main__":
    from akit. integration.dns.dnsconst import DnsKnownServiceTypes

    dns_query_services([DnsKnownServiceTypes.SONOS])