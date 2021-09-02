"""
.. module:: capabilities
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing classes that enable the discovery of extensions

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

import inspect

from akit.exceptions import AKitSemanticError

def capability(timeout=None):

    def decorator(capability_property):

        capability_type = None

        signature = inspect.signature(capability_property)
        capability_context = signature.return_annotation

        if capability_context == inspect._empty:
            errmsg = "Parameters factories for 'integration' functions must have an annotated return type."
            raise AKitSemanticError(errmsg)
        else:
            if issubclass(capability_context, CapabilityAddOn):
                _, _, capability_type = capability_context.__args__

                capabilities_table = None
                owning_type = capability_property.__type__
                if not hasattr(owning_type, "capabilities"):
                    capabilities_table = {}
                    setattr(owning_type, "capabilities", capabilities_table)

                if capability_type in capabilities_table:
                    errmsg = "Duplicate capability property for type={}".format(capability_type)
                    raise AKitSemanticError(errmsg)

                
            else:
                raise AKitSemanticError("Capability properties must be of type 'CapabilityAddOn'.")

        def capability_call_validator(self):

            rtnval = capability_property(self)

            return rtnval

        return capability_call_validator

    return decorator

class CapabilityAddOn:
    """
    """

class MultiCapable:
    """
    """

    CAPABILITY_ADDONS = None

    def __init__(self):
        self._capability_registry = {}
        self._capability_active = {}
        return

    def capability_is_active(self, capability: str) -> bool:
        rtnval = False
        if capability in self._capability_registry:
            self._capability_registry[capability]
        return rtnval

    def capability_is_active(self, capability: str) -> bool:
        rtnval = capability in self._capability_registry
        return rtnval

    def capability_startup(self):
        
        return

