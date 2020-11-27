"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ContentDirectory1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ContentDirectory1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ContentDirectory:1'

    SERVICE_EVENT_VARIABLES = {
        "ContainerUpdateIDs": { "data_type": "string", "default": None, "allowed_list": None},
        "SystemUpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TransferIDs": { "data_type": "string", "default": None, "allowed_list": None},
    }


    def action_Browse(self, ObjectID, BrowseFlag, Filter, StartingIndex, RequestedCount, SortCriteria, extract_returns=True):
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

        out_params = self._proxy_call_action("Browse", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "NumberReturned", "TotalMatches", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_CreateObject(self, ContainerID, Elements, extract_returns=True):
        """
            Calls the CreateObject action.

            :returns: "ObjectID", "Result"
        """
        arguments = {
            "ContainerID": ContainerID,
            "Elements": Elements,
        }

        out_params = self._proxy_call_action("CreateObject", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ObjectID", "Result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_CreateReference(self, ContainerID, ObjectID, extract_returns=True):
        """
            Calls the CreateReference action.

            :returns: "NewID"
        """
        arguments = {
            "ContainerID": ContainerID,
            "ObjectID": ObjectID,
        }

        out_params = self._proxy_call_action("CreateReference", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_DeleteResource(self, ResourceURI, extract_returns=True):
        """
            Calls the DeleteResource action.

            :returns: "result"
        """
        arguments = {
            "ResourceURI": ResourceURI,
        }

        out_params = self._proxy_call_action("DeleteResource", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_DestroyObject(self, ObjectID, extract_returns=True):
        """
            Calls the DestroyObject action.

            :returns: "result"
        """
        arguments = {
            "ObjectID": ObjectID,
        }

        out_params = self._proxy_call_action("DestroyObject", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_ExportResource(self, SourceURI, DestinationURI, extract_returns=True):
        """
            Calls the ExportResource action.

            :returns: "TransferID"
        """
        arguments = {
            "SourceURI": SourceURI,
            "DestinationURI": DestinationURI,
        }

        out_params = self._proxy_call_action("ExportResource", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransferID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetSearchCapabilities(self, extract_returns=True):
        """
            Calls the GetSearchCapabilities action.

            :returns: "SearchCaps"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetSearchCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SearchCaps",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetSortCapabilities(self, extract_returns=True):
        """
            Calls the GetSortCapabilities action.

            :returns: "SortCaps"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetSortCapabilities", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("SortCaps",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetSystemUpdateID(self, extract_returns=True):
        """
            Calls the GetSystemUpdateID action.

            :returns: "Id"
        """
        arguments = { }

        out_params = self._proxy_call_action("GetSystemUpdateID", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Id",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_GetTransferProgress(self, TransferID, extract_returns=True):
        """
            Calls the GetTransferProgress action.

            :returns: "TransferStatus", "TransferLength", "TransferTotal"
        """
        arguments = {
            "TransferID": TransferID,
        }

        out_params = self._proxy_call_action("GetTransferProgress", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransferStatus", "TransferLength", "TransferTotal",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_ImportResource(self, SourceURI, DestinationURI, extract_returns=True):
        """
            Calls the ImportResource action.

            :returns: "TransferID"
        """
        arguments = {
            "SourceURI": SourceURI,
            "DestinationURI": DestinationURI,
        }

        out_params = self._proxy_call_action("ImportResource", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("TransferID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_Search(self, ContainerID, SearchCriteria, Filter, StartingIndex, RequestedCount, SortCriteria, extract_returns=True):
        """
            Calls the Search action.

            :returns: "Result", "NumberReturned", "TotalMatches", "UpdateID"
        """
        arguments = {
            "ContainerID": ContainerID,
            "SearchCriteria": SearchCriteria,
            "Filter": Filter,
            "StartingIndex": StartingIndex,
            "RequestedCount": RequestedCount,
            "SortCriteria": SortCriteria,
        }

        out_params = self._proxy_call_action("Search", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "NumberReturned", "TotalMatches", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_StopTransferResource(self, TransferID, extract_returns=True):
        """
            Calls the StopTransferResource action.

            :returns: "result"
        """
        arguments = {
            "TransferID": TransferID,
        }

        out_params = self._proxy_call_action("StopTransferResource", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args


    def action_UpdateObject(self, ObjectID, CurrentTagValue, NewTagValue, extract_returns=True):
        """
            Calls the UpdateObject action.

            :returns: "result"
        """
        arguments = {
            "ObjectID": ObjectID,
            "CurrentTagValue": CurrentTagValue,
            "NewTagValue": NewTagValue,
        }

        out_params = self._proxy_call_action("UpdateObject", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("result",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

