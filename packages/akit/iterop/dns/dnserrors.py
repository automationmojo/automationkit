"""
.. module:: dnserrors
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the error types utilized by the multicast DNS code.

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


from akit.exceptions import AKitCommunicationsProtocolError

class DnsDecodeError(AKitCommunicationsProtocolError):
    """
        Error raised when the decoding of a DNS response fails.
    """
class DnsNonUniqueNameException(AKitCommunicationsProtocolError):
    """
        A non-unique name was encountered.
    """

class DnsNamePartTooLongException(AKitCommunicationsProtocolError):
    """
        The name part was too long
    """

class DnsBadTypeInNameException(AKitCommunicationsProtocolError):
    """
        Bad type in name
    """
