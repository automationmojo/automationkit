"""
.. module:: landscapeintegrationlayer
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

from akit.coupling.basecoupling import BaseCoupling

from akit.exceptions import AKitSemanticError

class LandscapeIntegrationLayer:
    """

    """

    _activated_gate = None

    def __init__(self):
        self._ordered_roles = []

        self._integration_points_registered = {}

        self._integration_point_registration_counter = 0

        super().__init__()

        # We need to wait till we have initialized the landscape configuration
        # layer before we start registering integration points
        lscapeType = type(self)
        lscapeType.landscape_description.register_integration_points(self)

        return

    def register_integration_point(self, role: str, coupling: BaseCoupling):
        """
            This method should be called from the attach_to_environment methods from individual couplings
            in order to register the base level integrations.  Integrations can be hierarchical so it
            is only necessary to register the root level integration couplings, the descendant couplings can
            be called from the root level couplings.

            :param role: The name of a role to assign for a coupling.
            :param coupling: The coupling to register for the associated role.
        """
        lscapeType = type(self)

        lscapeType.landscape_lock.acquire()
        try:
            if role not in self._integration_points_registered:
                self._ordered_roles.append(role)
                self._integration_points_registered[role] = coupling

                self._integration_point_registration_counter += 1
            else:
                raise AKitSemanticError("A coupling with the role %r was already registered." % role) from None
        finally:
            lscapeType.landscape_lock.release()

        return

    def activate_integration(self):
        """
            Called in order to mark the configuration process as complete in order
            for the activation stage to begin and to make the activation level methods
            callable.
        """
        self._landscape_configured = True
        return
