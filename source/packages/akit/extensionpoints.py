
from typing import List

import inspect

from akit.compat import import_by_name
from akit.environment.variables import AKIT_VARIABLES


class AKitExtensionPoints:

    _extension_points_type = None
    _instance = None

    def __new__(cls):
        """
            Constructs new instances of the AKitExtensionPoints object from the :class:`AKitExtensionPoints`
            type or from a derived type that is found in the module specified in the :module:`akit.environment.variables`
            module or by setting the 'AKIT_CONFIG_EXTENSION_POINTS_MODULE' environment variable.
        """
        if cls._instance is None:
            if cls._extension_points_type is None:
                cls._instance = super(AKitExtensionPoints, cls).__new__(cls)
            else:
                cls._instance = super(AKitExtensionPoints, cls._extension_points_type).__new__(cls._extension_points_type)
            # Put any initialization here.
        return cls._instance

    def get_coupling_ssh_coord_integration_type(self):
        from akit.coupling.sshpoolcoordinatorintegration import SshPoolCoordinatorIntegration
        return SshPoolCoordinatorIntegration

    def get_coupling_upnp_coord_integration_type(self):
        from akit.coupling.upnpcoordinatorintegration import UpnpCoordinatorIntegration
        return UpnpCoordinatorIntegration

    def get_testplus_default_job_type(self):
        from akit.testing.testplus.testjob import DefaultTestJob
        return DefaultTestJob
    
    def get_landscape_type(self):
        from akit.interop.landscaping.landscape import Landscape
        return Landscape


def is_subclass_of_extension_points(cand_type):
    """
        Returns a boolean value indicating if the candidate type is a subclass
        of :class:`Landscape`.
    """
    is_scoep = False
    if inspect.isclass(cand_type) and issubclass(cand_type, AKitExtensionPoints):
        is_scoep = True
    return is_scoep


def load_and_set_extension_points_type(extpnts_module):
    """
        Scans the module provided for :class:`Landscape` derived classes and will
        take the first one and assign it as the current runtime landscape type.
    """
    class_items = inspect.getmembers(extpnts_module, is_subclass_of_extension_points)
    for _, cls_type in class_items:
        type_module_name = cls_type.__module__
        if type_module_name == extpnts_module.__name__:
            AKitExtensionPoints._extension_points_type = cls_type # pylint: disable=protected-access
            break
    return

if AKIT_VARIABLES.AKIT_CONFIG_EXTENSION_POINTS_MODULE != "akit.extensionpoints":
    ep_module_override = import_by_name(AKIT_VARIABLES.AKIT_CONFIG_EXTENSION_POINTS_MODULE)
    load_and_set_extension_points_type(ep_module_override)