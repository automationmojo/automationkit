
from typing import List

from enum import Enum

from akit.xfeature import FeatureMask, FeatureTag

class ConstraintKeys(str, Enum):
    REQUIRED_FEATURES = "required_features"
    EXCLUDED_FEATURES = "excluded_features"

class Constraints(FeatureMask):

    def __init__(self, *, required_features: List[FeatureTag]=None,
                       excluded_features: List[FeatureTag]=None,
                       checkout: bool=False, **kwargs):
        super().__init__(required_features=required_features,
                         excluded_features=excluded_features,
                         checkout=checkout, **kwargs)
        return

def merge_constraints(*args: Constraints) -> Constraints:
    """
        Takes a sequence of :class:`Contraints` objects and merges them into a single
        :class:`Constraints` object.

        ..note: In cases where this method is provided with constraints with overlapping
                values, the last constraint with a give value will overwrite any previous
                values.
    """

    combined: Constraints = Constraints()

    for av in args:
        combined.update(av)
    
    return combined
