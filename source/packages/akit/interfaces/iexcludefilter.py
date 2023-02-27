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

class IExcludeFilter:
    """
        The IExcludeFilter interface is used to provide a common interface for performing an
        exclude filter on objects.
    """

    def should_exclude(self, other: Any) -> bool:
        errmsg = "The 'IExcludeFilter' interface requires the 'should_exclude' method to be implemented."
        raise AKitNotImplementedError(errmsg) from None
