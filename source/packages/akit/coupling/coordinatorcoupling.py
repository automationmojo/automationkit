"""
.. module:: coordinatorcoupling
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`CoordinatorCoupling` class and associated reflection methods.
        The :class:`CoordinatorCoupling` derived classes can be used to integraton automation resources and roles
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

from typing import TYPE_CHECKING

import inspect

from akit.exceptions import AKitNotOverloadedError
from akit.coupling.integrationcoupling import IntegrationCoupling

# Types imported only for type checking purposes
if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

class CoordinatorCoupling(IntegrationCoupling):
    """
        The :class:`CoordinatorCoupling` object serves as the base object for the declaration of an
        automation integration coordinator coupling.
    """

    coordinator = None

    @classmethod
    def create_coordinator(cls, landscape: "Landscape") -> object:
        """
            This API is called so that the landscape can create a coordinator for a given coordinator
            integration role.
        """
        raise AKitNotOverloadedError("This method must be overridden by derived coordinator classes.") from None
