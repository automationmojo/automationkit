"""
.. module:: eventedvariablesink
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`EventedVariableSink` class which is used to act
               as a container for the evented variables for the instance of a class representing
               the state of a remote object that propagates evented variable values.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2022, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Any, Optional, Tuple, Union

from datetime import datetime

class EventedVariableSink:
    """
    """

    def __init__(self):
        self._moment_register = {}
        return

    def moment_lookup(self, mpath: str) -> Union[Tuple[datetime, Any], Tuple[None, None]]:
        """
        """

        rtnval = None, None

        if mpath in self._moment_register:
            rtnval = self._moment_register[mpath]

        return rtnval

    def moment_register(self, mpath: str, moment: datetime, context: Optional[Any]):
        """
        """
        
        self._moment_register[mpath] = (moment, context)
        
        return