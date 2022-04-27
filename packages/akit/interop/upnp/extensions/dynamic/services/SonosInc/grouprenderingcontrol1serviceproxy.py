"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class GroupRenderingControl1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'GroupRenderingControl1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:GroupRenderingControl:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "GroupMute": { "data_type": "boolean", "default": None, "allowed_list": None},
        "GroupVolume": { "data_type": "ui2", "default": None, "allowed_list": None},
        "GroupVolumeChangeable": { "data_type": "boolean", "default": None, "allowed_list": None},
    }

    def action_GetGroupMute(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetGroupMute action.

            :returns: "CurrentMute"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetGroupMute", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentMute",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetGroupVolume(self, InstanceID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetGroupVolume action.

            :returns: "CurrentVolume"
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        out_params = self.call_action("GetGroupVolume", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SetGroupMute(self, InstanceID, DesiredMute, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetGroupMute action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredMute": DesiredMute,
        }

        self.call_action("SetGroupMute", arguments=arguments, aspects=aspects)

        return

    def action_SetGroupVolume(self, InstanceID, DesiredVolume, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetGroupVolume action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredVolume": DesiredVolume,
        }

        self.call_action("SetGroupVolume", arguments=arguments, aspects=aspects)

        return

    def action_SetRelativeGroupVolume(self, InstanceID, Adjustment, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRelativeGroupVolume action.

            :returns: "NewVolume"
        """
        arguments = {
            "InstanceID": InstanceID,
            "Adjustment": Adjustment,
        }

        out_params = self.call_action("SetRelativeGroupVolume", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewVolume",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SnapshotGroupVolume(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SnapshotGroupVolume action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("SnapshotGroupVolume", arguments=arguments, aspects=aspects)

        return
