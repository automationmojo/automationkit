"""
.. module:: pkey
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains methods for detecting the type of a private key file and
               for working with private key files.

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

PUB_KEY_BEGIN_RSA_PKCS1 = "-----BEGIN RSA PUBLIC KEY-----"
PUB_KEY_END_RSA_PKCS1 = "-----END RSA PUBLIC KEY-----"

PRV_KEY_BEGIN_RSA_PKCS1 = "-----BEGIN RSA PRIVATE KEY-----"
PRV_KEY_END_RSA_PKCS1 = "-----END RSA PRIVATE KEY-----"

PUB_KEY_BEGIN_RSA_PKCS8 = "-----BEGIN PUBLIC KEY-----"
PUB_KEY_END_RSA_PKCS8 = "-----END PUBLIC KEY-----"

PRV_KEY_BEGIN_RSA_PKCS8 = "-----BEGIN PRIVATE KEY-----"
PRV_KEY_END_RSA_PKCS8 = "-----END PRIVATE KEY-----"

PRV_KEYENC_BEGIN_RSA_PKCS8 = "-----BEGIN ENCRYPTED PRIVATE KEY-----"
PRV_KEYENC_END_RSA_PKCS8 = "-----END ENCRYPTED PRIVATE KEY-----"

# ASCII magic "openssh-key-v1" plus null byte
"6f70656e7373682d6b65792d7631 00"

def detect_private_key_type(filename: str) -> str:
    """
        Inspects the private key file specified and determines the keytype found in the file.

        :param filename: The filename of a private key file.

        :returns: A string for the keytype
    """
    # pylint: disable=invalid-name,no-else-break

    with open(filename, 'r') as kf:
        lines = kf.readlines()

    keytype = None
    for ln in lines:
        if ln.find(PRV_KEY_BEGIN_RSA_PKCS1) > -1:
            keytype = "rsa-pkcs1"
            break
        elif ln.find(PRV_KEY_BEGIN_RSA_PKCS8) > -1:
            keytype = "rsa-pkcs8"
            break
        elif ln.find(PRV_KEYENC_BEGIN_RSA_PKCS8) > -1:
            keytype = "rsa-pkcs8-enc"
            break

    return keytype
