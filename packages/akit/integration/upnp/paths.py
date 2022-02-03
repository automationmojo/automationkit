"""
.. module:: paths
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing constants for different paths utilize by the code generator that are relative to the test framework.

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


import os

from akit.environment.variables import AKIT_VARIABLES

DIR_UPNP = os.path.dirname(__file__)


DIR_UPNP_EXTENSIONS = os.path.join(DIR_UPNP, "extensions")

DIR_UPNP_EXTENSIONS_STANDARD = os.path.join(DIR_UPNP_EXTENSIONS, "standard")
DIR_UPNP_EXTENSIONS_STANDARD_EMBEDDEDDEVICES = os.path.join(DIR_UPNP_EXTENSIONS_STANDARD, "embeddeddevices")
DIR_UPNP_EXTENSIONS_STANDARD_ROOTDEVICES = os.path.join(DIR_UPNP_EXTENSIONS_STANDARD, "rootdevices")
DIR_UPNP_EXTENSIONS_STANDARD_SERVICES = os.path.join(DIR_UPNP_EXTENSIONS_STANDARD, "services")

DIR_UPNP_GENERATOR = os.path.join(DIR_UPNP, "generator")

DIR_UPNP_GENERATOR_STANDARD = os.path.join(DIR_UPNP_GENERATOR, "standard")
DIR_UPNP_GENERATOR_STANDARD_EMBEDDEDDEVICES = os.path.join(DIR_UPNP_GENERATOR_STANDARD, "embeddeddevices")
DIR_UPNP_GENERATOR_STANDARD_ROOTDEVICES = os.path.join(DIR_UPNP_GENERATOR_STANDARD, "rootdevices")
DIR_UPNP_GENERATOR_STANDARD_SERVICES = os.path.join(DIR_UPNP_GENERATOR_STANDARD, "services")


DIR_UPNP_EXTENSIONS_INTEGRATION = os.path.join(AKIT_VARIABLES.AKIT_HOME_DIRECTORY, "upnp", "extensions")
if AKIT_VARIABLES.AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE is not None:
    DIR_UPNP_EXTENSIONS_INTEGRATION = AKIT_VARIABLES.AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE

DIR_UPNP_EXTENSIONS_INTEGRATION_EMBEDDEDDEVICES = os.path.join(DIR_UPNP_EXTENSIONS_INTEGRATION, "embeddeddevices")
DIR_UPNP_EXTENSIONS_INTEGRATION_ROOTDEVICES = os.path.join(DIR_UPNP_EXTENSIONS_INTEGRATION, "rootdevices")
DIR_UPNP_EXTENSIONS_INTEGRATION_SERVICES = os.path.join(DIR_UPNP_EXTENSIONS_INTEGRATION, "services")

DIR_UPNP_SCAN_INTEGRATION = os.path.join(AKIT_VARIABLES.AKIT_HOME_DIRECTORY, "upnp", "scan")
if AKIT_VARIABLES.AKIT_UPNP_SCAN_INTEGRATION_BASE is not None:
    DIR_UPNP_SCAN_INTEGRATION = AKIT_VARIABLES.AKIT_UPNP_SCAN_INTEGRATION_BASE

DIR_UPNP_SCAN_INTEGRATION_EMBEDDEDDEVICES = os.path.join(DIR_UPNP_SCAN_INTEGRATION, "embeddeddevices")
DIR_UPNP_SCAN_INTEGRATION_ROOTDEVICES = os.path.join(DIR_UPNP_SCAN_INTEGRATION, "rootdevices")
DIR_UPNP_SCAN_INTEGRATION_SERVICES = os.path.join(DIR_UPNP_SCAN_INTEGRATION, "services")
