__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Any, List, Protocol

from akit.exceptions import AKitNotImplementedError

class IExcludeFilter(Protocol):
    """
        The IExcludeFilter interface is used to provide a common interface for performing an
        exclude filter on objects.
    """

    def should_exclude(self, check_object: Any) -> bool:
        """
            Determines if a device matches an exclude criteria internalized in the filter object.
        
            :param check_object: The object to check for a match with the exclude criteria.
        """

    def filter(self, input_list: List[Any]) -> List[Any]:

        output_list = []

        for nxt_object in input_list:
            if not self.should_exclude(nxt_object):
                output_list.append(nxt_object)

        return output_list