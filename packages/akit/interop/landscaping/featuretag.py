
from typing import FrozenSet, List, Union, Optional

import bisect

from akit.exceptions import AKitSemanticError

class FeatureTagNodeMeta(type):

    def __new__(metacls, name, bases, namespace, **kwargs):
        cls = super().__new__(metacls, name, bases, namespace, **kwargs)
        cls.ID = cls.__qualname__.lower().replace(".", "/")
        return cls
    
    def __repr__(self):
        return "'{}'".format(self.ID)

class FeatureTag(metaclass=FeatureTagNodeMeta):
    ID = None

class FeaturedDevice:

    def __init__(self):

        self._feature_tags = []
        return

    @property
    def feature_tags(self) -> FrozenSet[str]:
        return frozenset(self._feature_tags)

    def extend_features(self, features_to_add: Union[List[FeatureTag], List[str]]):
        """
            Used by derived class and mixins to extend the feature tags associated with
            a devices.
        """

        if len(features_to_add) > 0:
            first_item = features_to_add[0]
            if isinstance(first_item, str):
                # We insert the features into the list sorted so we can make finding
                # features faster.
                for ft in features_to_add:
                    bisect.insort(self._feature_tags, ft)
            elif issubclass(first_item, FeatureTag):
                # We insert the features into the list sorted so we can make finding
                # features faster.
                for ft in features_to_add:
                    bisect.insort(self._feature_tags, ft.ID)
            else:
                errmsg = "The 'features_to_add' parameter must contain items of type 'FeatureTag' or 'str'. item={}".format(
                    repr(first_item)
                )
                raise AKitSemanticError(errmsg)

        return
    
    def has_all_features(self, feature_list: Union[List[FeatureTag], List[str]]):

        has_all = True

        if len(feature_list) == 0:
            errmsg = "has_all_features: 'feature_list' cannot be empty."
            raise AKitSemanticError(errmsg)

        first_item = feature_list[0]
        if isinstance(first_item, str):
            for feature in feature_list:
                fid = feature
                hasfeature = fid in self._feature_tags
                if not hasfeature:
                    has_all = False
                    break
        elif issubclass(first_item, FeatureTag):
            for feature in feature_list:
                fid = feature.ID
                hasfeature = fid in self._feature_tags
                if not hasfeature:
                    has_all = False
                    break
        else:
            errmsg = "The 'feature_list' parameter must contain items of type 'FeatureTag' or 'str'. item={}".format(
                repr(first_item)
            )
            raise AKitSemanticError(errmsg)

        return has_all

    def has_any_feature(self, feature_list: List[FeatureTag]):

        has_any = False

        if len(feature_list) == 0:
            errmsg = "has_all_features: 'feature_list' cannot be empty."
            raise AKitSemanticError(errmsg)

        first_item = feature_list[0]
        if isinstance(first_item, str):
            for feature in feature_list:
                fid = feature

                hasfeature = fid in self._feature_tags
                if hasfeature:
                    has_any = True
                    break
        elif issubclass(first_item, FeatureTag):
            for feature in feature_list:
                fid = feature.ID

                hasfeature = fid in self._feature_tags
                if hasfeature:
                    has_any = True
                    break
        else:
            errmsg = "The 'feature_list' parameter must contain items of type 'FeatureTag' or 'str'. item={}".format(
                repr(first_item)
            )
            raise AKitSemanticError(errmsg)

        return has_any

    def has_feature(self, feature: Union[FeatureTag, str]):
        fid = None

        if isinstance(feature, str):
            fid = feature
        elif issubclass(feature, FeatureTag):
            fid = feature.ID
        else:
            errmsg = "The 'feature' parameter must be of type 'FeatureTag' or 'str'. item={}".format(
                repr(feature)
            )
            raise AKitSemanticError(errmsg)

        hasfeature = fid in self._feature_tags

        return hasfeature


KEY_REQUIRED_FEATURES = "required_features"
KEY_EXCLUDED_FEATURES = "excluded_features"


class FeatureMask(dict):

    def __init__(self, required_features: Optional[List[FeatureTag]]=None, excluded_features: Optional[List[FeatureTag]]=None, **kwargs):
        super().__init__(required_features=required_features, excluded_features=excluded_features, **kwargs)
        return


class FeatureFilter:

    def __init__(self, *, required_features: Optional[List[FeatureTag]]=None, excluded_features: Optional[List[FeatureTag]]=None, **kwargs):
        self._required_features = required_features
        self._excluded_features = excluded_features
        return

    def filter(self, device_list: List[FeaturedDevice]) -> List[FeaturedDevice]:

        matching_devices = []

        for fd in device_list:
            has_req_features = fd.has_all_features(self._required_features)
            has_excl_features = fd.has_any_feature(self._excluded_features)
            if has_req_features and not has_excl_features:
                matching_devices.append(fd)

        return matching_devices
