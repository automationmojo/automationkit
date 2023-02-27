__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Any

from akit.exceptions import AKitNotImplementedError

class IIncludeFilter:
    """
        The IIncludeFilter interface is used to provide a common interface for performing an
        include filter on objects.
    """

    def should_include(self, other: Any) -> bool:
        errmsg = "The 'IIncludeFilter' interface requires the 'should_include' method to be implemented."
        raise AKitNotImplementedError(errmsg) from None
