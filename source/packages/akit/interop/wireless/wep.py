__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import random

from enum import IntEnum
from string import hexdigits


class WEP_BIT_COUNT(IntEnum):
    BITS_64 = 64
    BITS_128 = 128
    BITS_152 = 152
    BITS_256 = 256

WEP_BITS_TO_HEX_CHARS = {
    WEP_BIT_COUNT.BITS_64: 5,
    WEP_BIT_COUNT.BITS_128: 13,
    WEP_BIT_COUNT.BITS_152: 16,
    WEP_BIT_COUNT.BITS_256: 29
}


def create_random_wep_key(bit_count: WEP_BIT_COUNT=WEP_BIT_COUNT.BITS_128):
    """
    """
    digit_count = WEP_BITS_TO_HEX_CHARS[bit_count]
    key = random.sample(hexdigits, digit_count)
    return key

