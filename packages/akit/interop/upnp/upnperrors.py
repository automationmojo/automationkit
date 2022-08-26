"""
.. module:: upnperrors
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the UPNP error classes.

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

from enum import Enum

from akit.exceptions import AKitCommunicationsProtocolError

class UpnpError(AKitCommunicationsProtocolError):
    """
        The base class for UPnP based errors.
    """
    def __init__(self, errorCode, errorDescription, extra=None):
        self.errorCode = errorCode
        self.errorDescription = errorDescription
        self.extra = extra

        errstr = "UpnpError: errorCode=%s errorDescription=%r " % (self.errorCode, self.errorDescription)
        if self.extra is not None:
            errstr += self.extra

        super(UpnpError, self).__init__(errstr)
        return

class UpnpErrorCodes(Enum):
    """
        An enumeration of the standard UPnP error codes
    """
    InvalidAction = 401
    InvalidArgs = 402
    DepricatedA = 403
    ActionFailed = 501
    ArgumentValueInvalid = 600
    ArgumentValueOutOfRange = 601
    OptionalActionNotImplemented = 602
    OutOfMemory = 603
    HumanInterventionRequired = 604
    StringArgumentTooLong = 605
    ActionNotAuthorized = 606
    SignatureFailure = 607
    SignatureMissing = 608
    NotEncrypted = 609
    InvalidSequence = 610
    InvalidControlURL = 611
    NoSuchSession = 612


UPNP_ERROR_TEST_LOOKUP = {
    401: "Invalid Action",
    402: "Invalid Arguments",
    403: "Depricated Error Code",
    501: "Action Failed",
    600: "Argument Value Invalid",
    601: "Argument Value Out of Range",
    602: "Optional Action Not Implemented",
    603: "Out of Memory",
    604: "Human Intervention Required",
    605: "String Argument Too Long",
    606: 'Action Not Authorized',
    607: 'Signature Failure',
    608: 'Signature Missing',
    609: 'Not Encrypted',
    610: 'Invalid Sequence',
    611: 'Invalid Control URL',
    612: 'No Such Session'
}

# 606-6124 Reserved These ErrorCodes are reserved for UPnP DeviceSecurity.
# 613-699 TBD Common action errors. Defined by UPnP Forum Technical Committee.
# 700-799 TBD Action-specific errors defined by UPnP Forum working committee.
# 800-899 TBD Action-specific errors for non-standard actions. Defined by UPnP vendor.
