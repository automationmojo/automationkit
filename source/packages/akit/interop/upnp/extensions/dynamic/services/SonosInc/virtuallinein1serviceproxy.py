"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class VirtualLineIn1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'VirtualLineIn1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:VirtualLineIn:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AVTransportURIMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTrackMetaData": { "data_type": "string", "default": None, "allowed_list": None},
        "CurrentTransportActions": { "data_type": "string", "default": None, "allowed_list": None},
        "EnqueuedTransportURIMetaData": { "data_type": "string", "default": None, "allowed_list": None},
    }

    SERVICE_EVENT_VARIABLES = {
        "LastChange": { "data_type": "string", "default": None, "allowed_list": None},
    }

    def action_Next(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Next action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Next", arguments=arguments, aspects=aspects)

        return

    def action_Pause(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Pause action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Pause", arguments=arguments, aspects=aspects)

        return

    def action_Play(self, InstanceID, Speed, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Play action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "Speed": Speed,
        }

        self.call_action("Play", arguments=arguments, aspects=aspects)

        return

    def action_Previous(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Previous action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Previous", arguments=arguments, aspects=aspects)

        return

    def action_SetVolume(self, InstanceID, DesiredVolume, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetVolume action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "DesiredVolume": DesiredVolume,
        }

        self.call_action("SetVolume", arguments=arguments, aspects=aspects)

        return

    def action_StartTransmission(self, InstanceID, CoordinatorID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartTransmission action.

            :returns: "CurrentTransportSettings"
        """
        arguments = {
            "InstanceID": InstanceID,
            "CoordinatorID": CoordinatorID,
        }

        out_params = self.call_action("StartTransmission", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTransportSettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_Stop(self, InstanceID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Stop action.
        """
        arguments = {
            "InstanceID": InstanceID,
        }

        self.call_action("Stop", arguments=arguments, aspects=aspects)

        return

    def action_StopTransmission(self, InstanceID, CoordinatorID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StopTransmission action.
        """
        arguments = {
            "InstanceID": InstanceID,
            "CoordinatorID": CoordinatorID,
        }

        self.call_action("StopTransmission", arguments=arguments, aspects=aspects)

        return
