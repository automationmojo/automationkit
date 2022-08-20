
from typing import List

from akit.interop.landscaping.featuretag import FeatureTag

class Constraints(dict):

    def __init__(self, required_features: List[FeatureTag]=None,
                       excluded_features: List[FeatureTag]=None,
                       checkout: bool=False, **kwargs):
        super().__init__(required_features=required_features,
                         excluded_features=excluded_features,
                         checkout=checkout, **kwargs)
        return
