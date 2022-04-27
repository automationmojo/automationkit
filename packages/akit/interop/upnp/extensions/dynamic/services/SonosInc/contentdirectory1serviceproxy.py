"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ContentDirectory1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ContentDirectory1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ContentDirectory:1'

    SERVICE_DEFAULT_VARIABLES = {
        "SearchCapabilities": { "data_type": "string", "default": None, "allowed_list": None},
        "SortCapabilities": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "Browseable": { "data_type": "boolean", "default": None, "allowed_list": None},
        "ContainerUpdateIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "FavoritePresetsUpdateID": { "data_type": "string", "default": None, "allowed_list": None},
        "FavoritesUpdateID": { "data_type": "string", "default": None, "allowed_list": None},
        "RadioFavoritesUpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "RadioLocationUpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "RecentlyPlayedUpdateID": { "data_type": "string", "default": None, "allowed_list": None},
        "SavedQueuesUpdateID": { "data_type": "string", "default": None, "allowed_list": None},
        "ShareIndexInProgress": { "data_type": "boolean", "default": None, "allowed_list": None},
        "ShareIndexLastError": { "data_type": "string", "default": None, "allowed_list": None},
        "ShareListUpdateID": { "data_type": "string", "default": None, "allowed_list": None},
        "SystemUpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "UserRadioUpdateID": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_Browse(self, ObjectID, BrowseFlag, Filter, StartingIndex, RequestedCount, SortCriteria, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Browse action.

            :returns: "Result", "NumberReturned", "TotalMatches", "UpdateID"
        """
        arguments = {
            "ObjectID": ObjectID,
            "BrowseFlag": BrowseFlag,
            "Filter": Filter,
            "StartingIndex": StartingIndex,
            "RequestedCount": RequestedCount,
            "SortCriteria": SortCriteria,
        }

        out_params = self.call_action("Browse", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "NumberReturned", "TotalMatches", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_CreateObject(self, ContainerID, Elements, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateObject action.

            :returns: "ObjectID", "Result"
        """
        arguments = {
            "ContainerID": ContainerID,
            "Elements": Elements,
        }

        out_params = self.call_action("CreateObject", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ObjectID", "Result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_DestroyObject(self, ObjectID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the DestroyObject action.
        """
        arguments = {
            "ObjectID": ObjectID,
        }

        self.call_action("DestroyObject", arguments=arguments, aspects=aspects)

        return

    def action_FindPrefix(self, ObjectID, Prefix, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the FindPrefix action.

            :returns: "StartingIndex", "UpdateID"
        """
        arguments = {
            "ObjectID": ObjectID,
            "Prefix": Prefix,
        }

        out_params = self.call_action("FindPrefix", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("StartingIndex", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAlbumArtistDisplayOption(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAlbumArtistDisplayOption action.

            :returns: "AlbumArtistDisplayOption"
        """
        arguments = { }

        out_params = self.call_action("GetAlbumArtistDisplayOption", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AlbumArtistDisplayOption",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAllPrefixLocations(self, ObjectID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAllPrefixLocations action.

            :returns: "TotalPrefixes", "PrefixAndIndexCSV", "UpdateID"
        """
        arguments = {
            "ObjectID": ObjectID,
        }

        out_params = self.call_action("GetAllPrefixLocations", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TotalPrefixes", "PrefixAndIndexCSV", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBrowseable(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBrowseable action.

            :returns: "IsBrowseable"
        """
        arguments = { }

        out_params = self.call_action("GetBrowseable", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("IsBrowseable",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLastIndexChange(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLastIndexChange action.

            :returns: "LastIndexChange"
        """
        arguments = { }

        out_params = self.call_action("GetLastIndexChange", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("LastIndexChange",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSearchCapabilities(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSearchCapabilities action.

            :returns: "SearchCaps"
        """
        arguments = { }

        out_params = self.call_action("GetSearchCapabilities", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SearchCaps",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetShareIndexInProgress(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetShareIndexInProgress action.

            :returns: "IsIndexing"
        """
        arguments = { }

        out_params = self.call_action("GetShareIndexInProgress", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("IsIndexing",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSortCapabilities(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSortCapabilities action.

            :returns: "SortCaps"
        """
        arguments = { }

        out_params = self.call_action("GetSortCapabilities", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SortCaps",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSystemUpdateID(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSystemUpdateID action.

            :returns: "Id"
        """
        arguments = { }

        out_params = self.call_action("GetSystemUpdateID", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Id",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RefreshShareIndex(self, AlbumArtistDisplayOption, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RefreshShareIndex action.
        """
        arguments = {
            "AlbumArtistDisplayOption": AlbumArtistDisplayOption,
        }

        self.call_action("RefreshShareIndex", arguments=arguments, aspects=aspects)

        return

    def action_RequestResort(self, SortOrder, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RequestResort action.
        """
        arguments = {
            "SortOrder": SortOrder,
        }

        self.call_action("RequestResort", arguments=arguments, aspects=aspects)

        return

    def action_SetBrowseable(self, Browseable, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetBrowseable action.
        """
        arguments = {
            "Browseable": Browseable,
        }

        self.call_action("SetBrowseable", arguments=arguments, aspects=aspects)

        return

    def action_UpdateObject(self, ObjectID, CurrentTagValue, NewTagValue, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the UpdateObject action.
        """
        arguments = {
            "ObjectID": ObjectID,
            "CurrentTagValue": CurrentTagValue,
            "NewTagValue": NewTagValue,
        }

        self.call_action("UpdateObject", arguments=arguments, aspects=aspects)

        return
