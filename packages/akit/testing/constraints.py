
from typing import List

from enum import Enum

from akit.xfeature import FeatureMask, FeatureTag

class ConstraintKeys(str, Enum):
    REQUIRED_FEATURES = "required_features"
    EXCLUDED_FEATURES = "excluded_features"

class Constraints(FeatureMask):

    def __init__(self, required_features: List[FeatureTag]=None,
                       excluded_features: List[FeatureTag]=None,
                       checkout: bool=False, **kwargs):
        super().__init__(required_features=required_features,
                         excluded_features=excluded_features,
                         checkout=checkout, **kwargs)
        return
