"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class Queue1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'Queue1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-sonos-com:service:Queue:1'

    SERVICE_DEFAULT_VARIABLES = {
        "Curated": { "data_type": "boolean", "default": None, "allowed_list": None},
        "UpdateID": { "data_type": "ui4", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddMultipleURIs(self, QueueID, UpdateID, ContainerURI, ContainerMetaData, DesiredFirstTrackNumberEnqueued, EnqueueAsNext, NumberOfURIs, EnqueuedURIsAndMetaData, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddMultipleURIs action.

            :returns: "FirstTrackNumberEnqueued", "NumTracksAdded", "NewQueueLength", "NewUpdateID"
        """
        arguments = {
            "QueueID": QueueID,
            "UpdateID": UpdateID,
            "ContainerURI": ContainerURI,
            "ContainerMetaData": ContainerMetaData,
            "DesiredFirstTrackNumberEnqueued": DesiredFirstTrackNumberEnqueued,
            "EnqueueAsNext": EnqueueAsNext,
            "NumberOfURIs": NumberOfURIs,
            "EnqueuedURIsAndMetaData": EnqueuedURIsAndMetaData,
        }

        out_params = self.call_action("AddMultipleURIs", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FirstTrackNumberEnqueued", "NumTracksAdded", "NewQueueLength", "NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AddURI(self, QueueID, UpdateID, EnqueuedURI, EnqueuedURIMetaData, DesiredFirstTrackNumberEnqueued, EnqueueAsNext, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddURI action.

            :returns: "FirstTrackNumberEnqueued", "NumTracksAdded", "NewQueueLength", "NewUpdateID"
        """
        arguments = {
            "QueueID": QueueID,
            "UpdateID": UpdateID,
            "EnqueuedURI": EnqueuedURI,
            "EnqueuedURIMetaData": EnqueuedURIMetaData,
            "DesiredFirstTrackNumberEnqueued": DesiredFirstTrackNumberEnqueued,
            "EnqueueAsNext": EnqueueAsNext,
        }

        out_params = self.call_action("AddURI", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("FirstTrackNumberEnqueued", "NumTracksAdded", "NewQueueLength", "NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_AttachQueue(self, QueueOwnerID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AttachQueue action.

            :returns: "QueueID", "QueueOwnerContext"
        """
        arguments = {
            "QueueOwnerID": QueueOwnerID,
        }

        out_params = self.call_action("AttachQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("QueueID", "QueueOwnerContext",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Backup(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Backup action.
        """
        arguments = { }

        self.call_action("Backup", arguments=arguments, aspects=aspects)

        return

    def action_Browse(self, QueueID, StartingIndex, RequestedCount, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Browse action.

            :returns: "Result", "NumberReturned", "TotalMatches", "UpdateID"
        """
        arguments = {
            "QueueID": QueueID,
            "StartingIndex": StartingIndex,
            "RequestedCount": RequestedCount,
        }

        out_params = self.call_action("Browse", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("Result", "NumberReturned", "TotalMatches", "UpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_CreateQueue(self, QueueOwnerID, QueueOwnerContext, QueuePolicy, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the CreateQueue action.

            :returns: "QueueID"
        """
        arguments = {
            "QueueOwnerID": QueueOwnerID,
            "QueueOwnerContext": QueueOwnerContext,
            "QueuePolicy": QueuePolicy,
        }

        out_params = self.call_action("CreateQueue", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("QueueID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RemoveAllTracks(self, QueueID, UpdateID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveAllTracks action.

            :returns: "NewUpdateID"
        """
        arguments = {
            "QueueID": QueueID,
            "UpdateID": UpdateID,
        }

        out_params = self.call_action("RemoveAllTracks", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RemoveTrackRange(self, QueueID, UpdateID, StartingIndex, NumberOfTracks, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveTrackRange action.

            :returns: "NewUpdateID"
        """
        arguments = {
            "QueueID": QueueID,
            "UpdateID": UpdateID,
            "StartingIndex": StartingIndex,
            "NumberOfTracks": NumberOfTracks,
        }

        out_params = self.call_action("RemoveTrackRange", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ReorderTracks(self, QueueID, StartingIndex, NumberOfTracks, InsertBefore, UpdateID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ReorderTracks action.

            :returns: "NewUpdateID"
        """
        arguments = {
            "QueueID": QueueID,
            "StartingIndex": StartingIndex,
            "NumberOfTracks": NumberOfTracks,
            "InsertBefore": InsertBefore,
            "UpdateID": UpdateID,
        }

        out_params = self.call_action("ReorderTracks", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ReplaceAllTracks(self, QueueID, UpdateID, ContainerURI, ContainerMetaData, CurrentTrackIndex, NewCurrentTrackIndices, NumberOfURIs, EnqueuedURIsAndMetaData, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ReplaceAllTracks action.

            :returns: "NewQueueLength", "NewUpdateID"
        """
        arguments = {
            "QueueID": QueueID,
            "UpdateID": UpdateID,
            "ContainerURI": ContainerURI,
            "ContainerMetaData": ContainerMetaData,
            "CurrentTrackIndex": CurrentTrackIndex,
            "NewCurrentTrackIndices": NewCurrentTrackIndices,
            "NumberOfURIs": NumberOfURIs,
            "EnqueuedURIsAndMetaData": EnqueuedURIsAndMetaData,
        }

        out_params = self.call_action("ReplaceAllTracks", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewQueueLength", "NewUpdateID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SaveAsSonosPlaylist(self, QueueID, Title, ObjectID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SaveAsSonosPlaylist action.

            :returns: "AssignedObjectID"
        """
        arguments = {
            "QueueID": QueueID,
            "Title": Title,
            "ObjectID": ObjectID,
        }

        out_params = self.call_action("SaveAsSonosPlaylist", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("AssignedObjectID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
