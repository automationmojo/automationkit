"""
.. module:: soap
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains classes and constants for working with SOAP message processing.

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

import enum
import re

from xml.etree.ElementTree import Element, SubElement, QName, ParseError
from xml.etree.ElementTree import tostring as xml_tostring
from xml.etree.ElementTree import fromstring as xml_fromstring
from xml.etree.ElementTree import register_namespace

from akit.compat import str_cast

from akit.exceptions import AKitCommunicationsProtocolError
from akit.interop.upnp.upnperrors import UPNP_ERROR_TEST_LOOKUP

NS_SOAP_ENV = "http://schemas.xmlsoap.org/soap/envelope/"
NS_SOAP_ENC = "http://schemas.xmlsoap.org/soap/encoding/"
NS_XSI = "http://www.w3.org/1999/XMLSchema-instance"
NS_XSD = "http://www.w3.org/1999/XMLSchema"

NS_UPNP_CONTROL = "urn:schemas-upnp-org:control-1-0"
NS_UPNP_EVENT = "urn:schemas-upnp-org:event-1-0"

URI_SOAP_ENCODING = "http://schemas.xmlsoap.org/soap/encoding/"

XML_DOCUMENT_DECLARATION = '<?xml version="1.0" encoding="utf-8"?>'

SOAP_TIMEOUT = 60

PYTHON_TO_SOAP_TYPE_MAP = {
    bytes: 'xsd:string',
    str: 'xsd:string',
    int: 'xsd:int',
    float: 'xsd:float',
    bool: 'xsd:boolean'
}

class SOAPError(AKitCommunicationsProtocolError):
    """
        Error that is raised when a Soap error occurs.
    """


class SOAPProtocolError(AKitCommunicationsProtocolError):
    """
        Error that is raised when a Soap protocol error occurs.
    """

def remove_extraneous_xml_declarations(xml_str):
    """
        Special method for correcting XML content that has an extra XML declaration.
    """
    xml_declaration = ''
    if xml_str.startswith('<?xml'):
        xml_declaration, xml_str = xml_str.split('?>', maxsplit=1)
    xml_declaration += '?>'
    xml_str = re.sub(r'<\?xml.*?\?>', '', xml_str, flags=re.I)
    return xml_declaration + xml_str

class SoapProcessor:
    """
        The Soap processor object stores encoding and decoding settings for processing the Soap messages
        senti to and from a UPNP device.
    """
    def __init__(self, encoding=URI_SOAP_ENCODING, envelope_attrib=None, typed=None):
        self._encoding = encoding
        self._envelope_attrib = envelope_attrib
        self._typed = typed
        return

    def create_request(self, action_name: str, arguments: dict, encoding=None, envelope_attrib=None, typed=None):
        """
            Creates a Soap request for a call on the specified action and with the specified arguments.
        """
        register_namespace('', None)

        if encoding is None:
            encoding = self._encoding
        if envelope_attrib is None:
            envelope_attrib = self._envelope_attrib
        if typed is None:
            typed = self._typed

        envelope = Element("s:Envelope")
        if envelope_attrib:
            for eakey, eaval in envelope_attrib:
                envelope.attrib.update({eakey: eaval})
        else:
            envelope.attrib.update({'xmlns:s': NS_SOAP_ENV})
            envelope.attrib.update({'s:encodingStyle': encoding})

        body = SubElement(envelope, "s:Body")

        if typed:
            methElement = SubElement(body, "u:" + action_name)
            methElement.attrib.update({'xmlns:u': typed})
        else:
            methElement = SubElement(body, action_name)

        if arguments:
            for arg_name, arg_val in arguments.items():
                if isinstance(arg_val, enum.Enum):
                    arg_val = arg_val.value

                py_type = type(arg_val)
                soap_type = PYTHON_TO_SOAP_TYPE_MAP[py_type]

                if soap_type == 'xsd:string':
                    arg_val = arg_val # pylint: disable=self-assigning-variable
                elif soap_type == 'xsd:int' or soap_type == 'xsd:float':
                    arg_val = str(arg_val)
                elif soap_type == 'xsd:boolean':
                    arg_val = "1" if arg_val else "0"

                argElement = SubElement(methElement, arg_name)
                #if typed and soap_type:
                #    if not isinstance(type, QName):
                #        soap_type = QName(NS_XSD, soap_type)
                #    argElement.set(NS_XSI + "type", soap_type)

                argElement.text = arg_val
        else:
            methElement.text = ""

        envelope_content = xml_tostring(envelope, short_empty_elements=False)
        content = XML_DOCUMENT_DECLARATION + str_cast(envelope_content)

        return content

    def create_response(self, action_name: str, arguments: dict, encoding=None, envelope_attrib=None, typed=None):
        """
            Creates a Soap response to the action with the specified arguments.
        """
        register_namespace('', None)

        if encoding is None:
            encoding = self._encoding
        if envelope_attrib is None:
            envelope_attrib = self._envelope_attrib
        if typed is None:
            typed = self._typed

        envelope = Element("s:Envelope")
        if envelope_attrib:
            for eakey, eaval in envelope_attrib:
                envelope.attrib.update({eakey: eaval})
        else:
            envelope.attrib.update({'xmlns:s': NS_SOAP_ENV})
            envelope.attrib.update({'s:encodingStyle': encoding})

        body = SubElement(envelope, "s:Body")

        action_name_tag_name = action_name + "Response"
        methElement = SubElement(body, action_name_tag_name)
        if encoding:
            methElement.set(NS_SOAP_ENV + "encodingStyle", encoding)

        if arguments:
            for arg_name, arg_val in arguments.items():
                py_type = type(arg_val)
                soap_type = PYTHON_TO_SOAP_TYPE_MAP[py_type]

                if soap_type == 'xsd:string':
                    arg_val = arg_val # pylint: disable=self-assigning-variable
                elif soap_type == 'xsd:int' or soap_type == 'xsd:float':
                    arg_val = str(arg_val)
                elif soap_type == 'xsd:boolean':
                    arg_val = "1" if arg_val else "0"

                argElement = SubElement(methElement, arg_name)
                if typed and soap_type:
                    if not isinstance(type, QName):
                        arg_type = QName(NS_XSD, soap_type)
                    argElement.set(NS_XSI + "type", soap_type)

                argElement.text = arg_val
        else:
            methElement.text = ""

        envelope_content = xml_tostring(envelope, short_empty_elements=False)
        content = XML_DOCUMENT_DECLARATION + "\n" + str_cast(envelope_content)

        return content

    def parse_response(self, action_name, content, encoding=None, envelope_attrib=None, typed=None):
        """
            Parses a response from the server with the given action name and content.
        """
        register_namespace('', None)

        if encoding is None:
            encoding = self._encoding
        if envelope_attrib is None:
            envelope_attrib = self._envelope_attrib
        if typed is None:
            typed = self._typed

        try:
            docNode = xml_fromstring(content)
        except ParseError:
            # Try removing any extra XML declarations in case there are more than one.
            # This sometimes happens when a device sends its own XML config files.
            content = remove_extraneous_xml_declarations(content)
            docNode = xml_fromstring(content)
        except ValueError:
            # This can occur when requests returns a `str` (unicode) but there's also an XML
            # declaration, which lxml doesn't like.
            docNode = xml_fromstring(content.encode('utf8'))

        resp_body = None
        if typed:
            resp_body = docNode.find(".//{%s}%sResponse" % (typed, action_name))
        else:
            resp_body = docNode.find(".//%sResponse" % action_name)

        if resp_body is None:
            msg = ('Returned XML did not include an element which matches namespace %r and tag name'
                   ' \'%sResponse\'.' % (typed, action_name))
            print(msg + '\n' + xml_tostring(docNode, short_empty_elements=False).decode('utf8'))
            raise SOAPProtocolError(msg)

        # Sometimes devices return XML strings as their argument values without escaping them with
        # CDATA. This checks to see if the argument has been parsed as XML and un-parses it if so.
        resp_dict = {}
        for arg in resp_body.getchildren():
            children = arg.getchildren()
            if children:
                resp_dict[arg.tag] = "\n".join(xml_tostring(x) for x in children)
            else:
                if arg.text is None:
                    resp_dict[arg.tag] = ""
                else:
                    resp_dict[arg.tag] = arg.text

        return resp_dict

    def parse_response_error_for_upnp(self, action_name, content, status_code, extra=None, encoding=None, envelope_attrib=None, typed=None):
        """
            Parse response error for a upnp response.
        """
        register_namespace('', None)

        if encoding is None:
            encoding = self._encoding
        if envelope_attrib is None:
            envelope_attrib = self._envelope_attrib
        if typed is None:
            typed = self._typed

        try:
            docNode = xml_fromstring(content)
        except ParseError:
            # Try removing any extra XML declarations in case there are more than one.
            # This sometimes happens when a device sends its own XML config files.
            content = remove_extraneous_xml_declarations(content)
            docNode = xml_fromstring(content)
        except ValueError:
            # This can occur when requests returns a `str` (unicode) but there's also an XML
            # declaration, which lxml doesn't like.
            docNode = xml_fromstring(content.encode('utf8'))

        resp_body = None
        if typed:
            resp_body = docNode.find(".//{%s}Fault" % (NS_SOAP_ENV,))
        else:
            resp_body = docNode.find(".//Fault")

        if resp_body is None:
            msg = ('Returned XML did not include an element which matches namespace %r and tag name'
                   ' \'%sFault\'.' % (typed, action_name))
            print(msg + '\n' + xml_tostring(docNode, short_empty_elements=False).decode('utf8'))
            raise SOAPProtocolError(msg)

        # Lets try to extract the XML response error information
        try:
            faultCode = resp_body.find(".//faultcode").text
            faultString = resp_body.find(".//faultstring").text
            detail = resp_body.find(".//detail")
            upnpErrorNode = detail.find(".//{%s}UPnPError" % NS_UPNP_CONTROL)
            errorCode = int(upnpErrorNode.find(".//{%s}errorCode" % NS_UPNP_CONTROL).text)
            errorDescription = upnpErrorNode.find(".//{%s}errorDescription" % NS_UPNP_CONTROL)
            if errorDescription is None:
                errorDescription = UPNP_ERROR_TEST_LOOKUP.get(errorCode, "Unknown error.")

        except Exception as xcpt:
            errmsg = "Unable to process xml response: status=%r\n%s" % (status_code, content)
            if extra is not None:
                errmsg += "EXTRA:\n%s" % extra
            raise SOAPProtocolError(errmsg) from xcpt

        return errorCode, errorDescription
