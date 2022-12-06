"""
.. module:: x509
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the classes and methods for working with X509 certificates.

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

from socket import gethostname
from typing import NamedTuple, Optional

from datetime import datetime

from OpenSSL import crypto


X509_DATETIME_FORMAT = '%Y%m%d%H%M%S%z'


class X509ExtensionInfo(NamedTuple):

    short_name: str
    data: str


class X509NameInfo(NamedTuple):

    country: str
    state_or_province: str
    locality: str
    organization: str
    unit: str
    common_name: str
    email_address: str


class X509CertificateInfo:

    def __init__(self, cert_obj: crypto.X509):
        self._cert_obj = cert_obj
        return

    @property
    def extensions(self):

        extdict = {}

        for ei in range(0, self._cert_obj.get_extension_count()):
            ext_obj = self._cert_obj.get_extension(ei)
            ex_short_name = ext_obj.get_short_name()
            ex_data = str(ext_obj)
            extdict[ex_short_name] = X509ExtensionInfo(ex_short_name, ex_data)

        return extdict

    @property
    def has_expired(self) -> bool:
        return self._cert_obj.has_expired()

    @property
    def issuer(self) -> X509NameInfo:
        iobj = self._cert_obj.get_issuer()
        iinfo = X509NameInfo(iobj.countryName, iobj.stateOrProvinceName, iobj.localityName, iobj.organizationName,
            iobj.organizationalUnitName, iobj.commonName, iobj.emailAddress)
        return iinfo
    
    @property
    def not_after(self) -> datetime:
        rtnval = self._cert_obj.get_notAfter()
        rtnval = datetime.strptime(rtnval, X509_DATETIME_FORMAT)
        return rtnval
    
    @property
    def not_before(self) -> datetime:
        rtnval = self._cert_obj.get_notBefore()
        rtnval = datetime.strptime(rtnval, X509_DATETIME_FORMAT)
        return rtnval

    @property
    def serial_no(self) -> int:
        rtnval = self._cert_obj.get_serial_number()
        return rtnval

    @property
    def sha256_digest(self) -> bytes:
        rtnval = self._cert_obj.digest("sha256")
        return rtnval

    @property
    def signature_algorithm(self) -> str:
        rtnval = self._cert_obj.get_signature_algorithm()
        return rtnval

    @property
    def subject(self) -> X509NameInfo:
        sobj = self._cert_obj.get_subject()
        sinfo = X509NameInfo(sobj.countryName, sobj.stateOrProvinceName, sobj.localityName, sobj.organizationName,
            sobj.organizationalUnitName, sobj.commonName, sobj.emailAddress)
        return sinfo

    @property
    def version(self) -> int:
        rtnval = self._cert_obj.get_version()
        return rtnval


def generate_self_signed_certificate(serial_no=1000, key_size=1024,
        country: Optional[str] = None, state_or_province: Optional[str] = None,
        locality: Optional[str] = None, organization: Optional[str] = None,
        unit: Optional[str] = None, common_name: Optional[str] = None,
        before_adjust_secs: Optional[int] = None, after_adjust_secs: Optional[int] = None):
    
    if country is None:
        country = "United States"
    if state_or_province is None:
        state_or_province = "Jefferson"
    if locality is None:
        locality = "Happy Camp"
    if organization is None:
        organization = "Automation Mojo"
    if unit is None:
        unit = "Automation Kit"
    if common_name is None:
        common_name = gethostname()

    # Create a key pair
    kp = crypto.PKey()
    kp.generate_key(crypto.TYPE_RSA, key_size)

    # Ceate a self-signed certificate
    cert = crypto.X509()

    subject = cert.get_subject()
    subject.C = country
    subject.ST = state_or_province
    subject.L = locality
    subject.O = organization
    subject.OU = unit
    subject.CN = common_name

    cert.set_serial_number(serial_no)

    if before_adjust_secs is None:
        before_adjust_secs = 0
    cert.gmtime_adj_notBefore(before_adjust_secs) # now

    if after_adjust_secs is None:
        years, days, hours, min, sec = 10, 365, 24, 60, 60
        after_adjust_secs = years * days * hours * min * sec
    cert.gmtime_adj_notAfter(after_adjust_secs)

    cert.set_issuer(subject)
    cert.set_pubkey(kp)

    cert.sign(kp, "sha1")

    # Create a P12 container
    p12 = crypto.PKCS12()
    p12.set_certificate(cert)

    cert_data = p12.export()

    return cert_data


def generate_signed_certificate(sig_key: crypto.PKey, issuer: crypto.X509Name, serial_no = 1000,
        key_size = 1024, country: Optional[str] = None, state_or_province: Optional[str] = None,
        locality: Optional[str] = None, organization: Optional[str] = None,
        unit: Optional[str] = None, common_name: Optional[str] = None,
        before_adjust_secs: Optional[int] = None, after_adjust_secs: Optional[int] = None):
    
    if country is None:
        country = "United States"
    if state_or_province is None:
        state_or_province = "Jefferson"
    if locality is None:
        locality = "Happy Camp"
    if organization is None:
        organization = "Automation Mojo"
    if unit is None:
        unit = "Automation Kit"
    if common_name is None:
        common_name = gethostname()

    # Create a key pair
    kp = crypto.PKey()
    kp.generate_key(crypto.TYPE_RSA, key_size)

    # Ceate a self-signed certificate
    cert = crypto.X509()

    subject = cert.get_subject()
    subject.C = country
    subject.ST = state_or_province
    subject.L = locality
    subject.O = organization
    subject.OU = unit
    subject.CN = common_name

    cert.set_serial_number(serial_no)

    if before_adjust_secs is None:
        before_adjust_secs = 0
    cert.gmtime_adj_notBefore(before_adjust_secs) # now

    if after_adjust_secs is None:
        years, days, hours, min, sec = 10, 365, 24, 60, 60
        after_adjust_secs = years * days * hours * min * sec
    cert.gmtime_adj_notAfter(after_adjust_secs)

    cert.set_pubkey(kp)

    cert.set_issuer(issuer)
    cert.sign(sig_key, "sha1")

    # Create a P12 container
    p12 = crypto.PKCS12()
    p12.set_certificate(cert)

    cert_data = p12.export()

    return cert_data