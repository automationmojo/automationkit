"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.extensible import LoadableExtension
from akit.integration.upnp.services.upnpserviceproxy import UpnpServiceProxy

class ExternalActivity1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'ExternalActivity1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:ExternalActivity:1'


    def action_Register(self, ButtonNameIn, DisplayStringIn, DurationIn, extract_returns=True):
        """
            Calls the Register action.

            :returns: "ActualDurationOut", "RegistrationIDOut"
        """
        arguments = {
            "ButtonNameIn": ButtonNameIn,
            "DisplayStringIn": DisplayStringIn,
            "DurationIn": DurationIn,
        }

        out_params = self.proxy_call_action("Register", arguments=arguments)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("ActualDurationOut", "RegistrationIDOut",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
