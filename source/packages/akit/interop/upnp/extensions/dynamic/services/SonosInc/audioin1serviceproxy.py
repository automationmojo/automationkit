"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class AudioIn1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'AudioIn1' service.
    """

    SERVICE_MANUFACTURER = 'SonosInc'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:AudioIn:1'

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {
        "AudioInputName": { "data_type": "string", "default": None, "allowed_list": None},
        "Icon": { "data_type": "string", "default": None, "allowed_list": None},
        "LeftLineInLevel": { "data_type": "i4", "default": None, "allowed_list": None},
        "LineInConnected": { "data_type": "boolean", "default": None, "allowed_list": None},
        "Playing": { "data_type": "boolean", "default": None, "allowed_list": None},
        "RightLineInLevel": { "data_type": "i4", "default": None, "allowed_list": None},
    }

    def action_GetAudioInputAttributes(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAudioInputAttributes action.

            :returns: "CurrentName", "CurrentIcon"
        """
        arguments = { }

        out_params = self.call_action("GetAudioInputAttributes", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentName", "CurrentIcon",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLineInLevel(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLineInLevel action.

            :returns: "CurrentLeftLineInLevel", "CurrentRightLineInLevel"
        """
        arguments = { }

        out_params = self.call_action("GetLineInLevel", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentLeftLineInLevel", "CurrentRightLineInLevel",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_SelectAudio(self, ObjectID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SelectAudio action.
        """
        arguments = {
            "ObjectID": ObjectID,
        }

        self.call_action("SelectAudio", arguments=arguments, aspects=aspects)

        return

    def action_SetAudioInputAttributes(self, DesiredName, DesiredIcon, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAudioInputAttributes action.
        """
        arguments = {
            "DesiredName": DesiredName,
            "DesiredIcon": DesiredIcon,
        }

        self.call_action("SetAudioInputAttributes", arguments=arguments, aspects=aspects)

        return

    def action_SetLineInLevel(self, DesiredLeftLineInLevel, DesiredRightLineInLevel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetLineInLevel action.
        """
        arguments = {
            "DesiredLeftLineInLevel": DesiredLeftLineInLevel,
            "DesiredRightLineInLevel": DesiredRightLineInLevel,
        }

        self.call_action("SetLineInLevel", arguments=arguments, aspects=aspects)

        return

    def action_StartTransmissionToGroup(self, CoordinatorID, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StartTransmissionToGroup action.

            :returns: "CurrentTransportSettings"
        """
        arguments = {
            "CoordinatorID": CoordinatorID,
        }

        out_params = self.call_action("StartTransmissionToGroup", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("CurrentTransportSettings",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_StopTransmissionToGroup(self, CoordinatorID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the StopTransmissionToGroup action.
        """
        arguments = {
            "CoordinatorID": CoordinatorID,
        }

        self.call_action("StopTransmissionToGroup", arguments=arguments, aspects=aspects)

        return
