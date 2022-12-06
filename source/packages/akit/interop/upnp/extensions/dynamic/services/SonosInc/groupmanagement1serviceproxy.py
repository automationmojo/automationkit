"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class GroupManagement1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'GroupManagement1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:GroupManagement:1'

    SERVICE_DEFAULT_VARIABLES = {
        "SourceAreaIds": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "GroupCoordinatorIsLocal": { "data_type": "boolean", "default": None, "allowed_list": None},
        "LocalGroupUUID": { "data_type": "string", "default": None, "allowed_list": None},
        "ResetVolumeAfter": { "data_type": "boolean", "default": None, "allowed_list": None},
        "VirtualLineInGroupID": { "data_type": "string", "default": None, "allowed_list": None},
        "VolumeAVTransportURI": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_AddMember(self, MemberID, BootSeq, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the AddMember action.

            :returns: "CurrentTransportSettings", "CurrentURI", "GroupUUIDJoined", "ResetVolumeAfter", "VolumeAVTransportURI"
        """
        arguments = {
            "MemberID": MemberID,
            "BootSeq": BootSeq,
        }

        out_params = self.call_action("AddMember", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTransportSettings", "CurrentURI", "GroupUUIDJoined", "ResetVolumeAfter", "VolumeAVTransportURI",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_RemoveMember(self, MemberID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the RemoveMember action.
        """
        arguments = {
            "MemberID": MemberID,
        }

        self.call_action("RemoveMember", arguments=arguments, aspects=aspects)

        return

    def action_ReportTrackBufferingResult(self, MemberID, ResultCode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ReportTrackBufferingResult action.
        """
        arguments = {
            "MemberID": MemberID,
            "ResultCode": ResultCode,
        }

        self.call_action("ReportTrackBufferingResult", arguments=arguments, aspects=aspects)

        return

    def action_SetSourceAreaIds(self, DesiredSourceAreaIds, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetSourceAreaIds action.
        """
        arguments = {
            "DesiredSourceAreaIds": DesiredSourceAreaIds,
        }

        self.call_action("SetSourceAreaIds", arguments=arguments, aspects=aspects)

        return
