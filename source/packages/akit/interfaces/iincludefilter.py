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

class IIncludeFilter(Protocol):
    """
        The IIncludeFilter interface is used to provide a common interface for performing an
        include filter on objects.
    """

    def should_include(self, check_object: Any) -> bool:
        """
            Determines if a device matches an include criteria internalized in the filter object.

            :param check_object: The object to check for a match with the exclude criteria.
        """
    
    def filter(self, input_list: List[Any]) -> List[Any]:

        output_list = []

        for nxt_object in input_list:
            if self.should_include(nxt_object):
                output_list.append(nxt_object)

        return output_list
