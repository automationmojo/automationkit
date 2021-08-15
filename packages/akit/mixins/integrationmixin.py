"""
.. module:: integration
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`IntegrationMixIn` class and associated reflection methods.
        The :class:`IntegrationMixIn` derived classes can be used to integraton automation resources and roles
        into the test environment.

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

from typing import Dict, List, Tuple

import inspect

from akit.exceptions import AKitNotOverloadedError

from akit.mixins.basemixin import BaseMixIn

from akit.xlogging.foundations import getAutomatonKitLogger

class IntegrationMixIn(BaseMixIn):
    """
        The :class:`IntegrationMixIn` object serves as the base object for the declaration of an
        automation integration requirement.  The :class:`akit.testing.unittest.testsequencer.Sequencer`
        queries the class hierarchies of the tests that are included in an automation run.
    """

    landscape = None

    logger = None
    pathbase = None

    CONSTRAINTS = None

    def __init__(self, *args, role=None, **kwargs): # pylint: disable=unused-argument
        """
            The default contructor for an :class:`IntegrationMixIn`.
        """
        super(IntegrationMixIn, self).__init__()

        self._role = role
        self._connectivity_establish = False
        self._presence_establish = False

        if self.pathbase is None:
            err_msg = "The 'pathbase' class member variable must be set to a unique name for each integration class type."
            raise ValueError(err_msg)

        self.context.insert(self.pathbase, self)
        return

    @property
    def connectivity_establish(self):
        return self._connectivity_establish

    @property
    def mode(self):
        """
            Returns the current mode any associated resource is operating in.
        """
        return self._mode

    @mode.setter
    def mode(self, value):
        """
            Sets the current mode any associated resource is operating in.
        """
        old_value = self._mode
        self._mode = value
        self.on_mode_changed(old_value, value)
        return

    @property
    def presence_establish(self):
        return self._presence_establish

    @property
    def role(self):
        """
            Returns the current automation role assigned to the integration mixin.
        """
        return self._role

    def on_mode_changed(self, prev_mode, new_mode): # pylint: disable=no-self-use,unused-argument
        """
            Implemented by derived classes in order to perform the changeover of modes.
        """
        return

    @classmethod
    def declare_precedence(cls) -> int:
        """
            This API is called so that the IntegrationMixIn can declare an ordinal precedence that should be
            utilized for bringing up its integration state.
        """
        cls.logger = getAutomatonKitLogger()
        return

    @classmethod
    def attach_to_environment(cls, constraints: Dict={}):
        """
            This API is called so that the IntegrationMixIn can process configuration information.  The :class:`IntegrationMixIn`
            will verify that it has a valid environment and configuration to run in.

            :raises :class:`akit.exceptions.AKitMissingConfigError`, :class:`akit.exceptions.AKitInvalidConfigError`:
        """
        raise AKitNotOverloadedError("The 'attach_to_environment' method must be overloaded by derived integration mixin types.")
    
    @classmethod
    def attach_to_framework(cls, landscape: "Landscape"):
        """
            This API is called so that the IntegrationMixIn can attach to the test framework and participate with
            registration processes.  This allows the framework to ignore the bring-up of mixins that are not being
            included by a test.
        """
        cls.landscape = landscape
        return

    @classmethod
    def collect_resources(cls):
        """
            This API is called so the `IntegrationMixIn` can connect with a resource management
            system and gain access to the resources required for the automation run.

            :raises :class:`akit.exceptions.AKitResourceError`:
        """
        raise AKitNotOverloadedError("The 'collect_resources' method must be overloaded by derived integration mixin types.")

    @classmethod
    def diagnostic(cls, diag_level: int, diag_folder: str): # pylint: disable=unused-argument
        """
            The API is called by the :class:`akit.sequencer.Sequencer` object when the automation sequencer is
            building out a diagnostic package at a diagnostic point in the automation sequence.  Example diagnostic
            points are:

            * pre-run
            * post-run

            Each diagnostic package has its own storage location so derived :class:`akit.scope.ScopeMixIn` objects
            can simply write to their specified output folder.

            :param diag_level: The maximum diagnostic level to run dianostics for.
            :param diag_folder: The output folder path where the diagnostic information should be written.
        """
        return

    @classmethod
    def establish_connectivity(cls, allow_missing_devices: bool=False) -> Tuple[List[str], Dict]:
        """
            This API is called so the `IntegrationMixIn` can establish connectivity with any compute or storage
            resources.

            :returns: A tuple with a list of error messages for failed connections and dict of connectivity
                      reports for devices devices based on the coordinator.
        """
        raise AKitNotOverloadedError("The 'diagnostic' method must be overloaded by derived integration mixin types.")

    @classmethod
    def establish_presence(cls) -> Tuple[List[str], Dict]:
        """
            This API is called so the `IntegrationMixIn` can establish presence with any compute or storage
            resources.

            :returns: A tuple with a list of error messages for failed connections and dict of connectivity
                      reports for devices devices based on the coordinator.
        """
        raise AKitNotOverloadedError("The 'diagnostic' method must be overloaded by derived integration mixin types.")


def is_integration_mixin(cls):
    """
        Helper function that is used to determine if a type is an :class:`IntegrationMixIn` subclass, but not
        the :class:`IntegrationMixIn` type itself.
    """
    is_integmi = False
    if inspect.isclass(cls) and cls is not IntegrationMixIn and issubclass(cls, IntegrationMixIn):
        is_integmi = True
    return is_integmi

def sort_integration_mixins_by_precedence(self, mixin_list: List[IntegrationMixIn]) -> List[IntegrationMixIn]:
    """
        Takes a list of :class:`IntegrationMixIn` classes and creates an ordered list based on the ordinal
        precedence declared by the :class:`IntegrationMixIn`.
    """
    precedence_table = {}

    for mixin in mixin_list:
        precedence = mixin.declare_precedence()
        precedence_level_list = None
        if precedence in precedence_table:
            precedence_level_list = precedence_table[precedence]
        else:
            precedence_level_list = []
            precedence_table[precedence] = precedence_level_list
        precedence_level_list.append(mixin)

    precedence_keys_sorted = precedence_table.keys()
    precedence_keys_sorted.sort()

    ordered_mixins = []
    for precedence in precedence_keys_sorted:
        ordered_mixins.extend(precedence_table[precedence])

    return ordered_mixins