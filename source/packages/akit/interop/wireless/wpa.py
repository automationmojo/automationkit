
from string import ascii_lowercase, ascii_uppercase, digits

# We might want to write any generated passwords into a log or config file
# so don't use all the printable characters.  The security offered by these
# charaters is sufficient for automation purposes
WPA_USEABLE_CHARACTERS =  ascii_lowercase + ascii_uppercase + digits

WPA_MIN_CHAR_COUNT = 8
WPA_MAX_CHAR_COUNT = 63

import random

def create_random_wpa_password():
    """
    """
    char_count = random.choice(range(WPA_MIN_CHAR_COUNT, WPA_MAX_CHAR_COUNT))
    key = random.sample(WPA_USEABLE_CHARACTERS, char_count)
    return key