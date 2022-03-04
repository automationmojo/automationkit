"""
.. module:: landscapebaselayer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the Landscape related classes.

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

import threading

from akit.environment.context import Context

from akit.integration.landscaping.landscapedescription import LandscapeDescription
from akit.integration.landscaping.landscapedevice import LandscapeDevice
from akit.integration.landscaping.landscapedeviceextension import LandscapeDeviceExtension
from akit.integration.landscaping.topologydescription import TopologyDescription

from akit.xlogging.foundations import getAutomatonKitLogger

class LandscapeBaseLayer:

    context = Context()

    logger = getAutomatonKitLogger()
    landscape_lock = threading.RLock()

    landscape_description = LandscapeDescription
    landscape_device = LandscapeDevice
    landscape_device_extension = LandscapeDeviceExtension

    topology_description = TopologyDescription
