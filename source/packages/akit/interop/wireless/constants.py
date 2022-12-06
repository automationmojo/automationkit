
from typing import NamedTuple

from enum import IntEnum, Enum

REGION_CODES = [
    "AE", "AR", "AT", "AU", "BG", "BH", "BM", "BO", "BR", "CA", "CH", "CL",
    "CN", "CO", "CR", "CS", "CY", "CZ", "DE", "DK", "DO", "DZ", "EC", "EE",
    "EG", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "ID", "IE", "IL",
    "IN", "IS", "IT", "JM", "JO", "KE", "KR", "KW", "KW", "LB", "LI", "LI",
    "LK", "LT", "LT", "LU", "MA", "MA", "MU", "MX", "MX", "NL", "NO", "NZ",
    "NZ", "OM", "PA", "PA", "PE", "PH", "PK", "PL", "PL", "PR", "PR", "PT",
    "QA", "RO", "RU", "RU", "SA", "SG", "SI", "SI", "SK", "SK", "SV", "TH",
    "TH", "TN", "TR", "TT", "TW", "UA", "US", "UY", "UY", "VE", "VN", "ZA"
]

DEFAULT_REGION_CODE = 'US'

class DeAuthenticationReason(IntEnum):
    """
        Reason code that is provided when an access point de-authenticates with a client. (IEEE 802.11)
    """
    PREV_AUTH_NOT_VALID = 2
    STA_LEAVE_IBBS = 3
    STA_INACTIVE = 4
    AP_OVERLOADED = 5
    STA_NOT_ASSOCIATED = 7
    STA_LEAVE_BSS = 8

class MfpMode(IntEnum):
    """
        OpenWRT AP settings for the Management Frame Protection (MFP) or
        Protected Management Frames (PMF) from standard IEEE 802.11w-2009.
    """
    DISABLED = 0
    OPTIONAL = 1
    REQUIRED = 2

class OpenWrtModel(str, Enum):
    NETGEAR_7600 = 'ipq806x'
    NETGEAR_WNDR3700 = 'ar71xx'
    NETGEAR_WNDR3700_1907 = 'ath79'


class WirelessEncryption(str, Enum):
    """
        Wireless encryption modes supported by routers running the OpenWRT firmware.
    """
    WEP = "wep"
    WEP_OPEN = "wep+open"
    WEP_MIXED = "wep+mixed"
    WPA2_TKIP_CCMP = "psk2+tkip+ccmp"
    WPA2_TKIP_AES = "psk2+tkip+aes"
    WPA2_TKIP = "psk2+tkip"
    WPA2_CCMP = "psk2+ccmp"
    WPA2_AES = "psk2+aes"
    WPA2 = "psk2"
    WPA_TKIP_CCMP = "psk+tkip+ccmp"
    WPA_TKIP_AES = "psk+tkip+aes"
    WPA_TKIP= "psk+tkip"
    WPA_CCMP = "psk+ccmp"
    WPA_AES = "psk+aes"
    WPA = "psk"
    WPA_MIXED_TKIP_CCMP = "mixed-psk+tkip+ccmp"
    WPA_MIXED_TKIP_AES = "mixed-psk+tkip+aes"
    WPA_MIXED = "mixed-psk"
    WPA_MIXED_TKIP = "mixed-psk+tkip"
    WPA_MIXED_CCMP = "mixed-psk+ccmp"
    WPA_MIXED_AES = "mixed-psk+aes"
    WEP_SHARED = "wep-shared"
    OPEN = "none"
    WPA3 = "sae"
    WPA3_MIXED = "sae-mixed"
