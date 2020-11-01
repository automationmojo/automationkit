"""
.. module:: akit.integration.upnp.extensions.sonos.zpssub
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the a Upnp device for a Sonos ZpsSub.

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

from akit.extensible import LoadableExtension

from akit.integration.upnp.extensions.standard.rootdevices.sonos.sonosdevice import SonosPlayer
from akit.integration.upnp.devices.upnprootdevice import UpnpRootDevice

class SonosDeviceZpSub(SonosPlayer, LoadableExtension):
    """
    """

    MANUFACTURER = "Sonos, Inc."
    MODEL_NUMBER = "Sub"
    MODEL_DESCRIPTION = "Sonos Sub"

