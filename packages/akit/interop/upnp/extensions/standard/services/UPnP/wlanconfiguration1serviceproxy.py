"""

    NOTE: This is a code generated file.  This file should not be edited directly.
"""



from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class WLANConfiguration1ServiceProxy(UpnpServiceProxy, LoadableExtension):
    """
        This is a code generated proxy class to the 'WLANConfiguration1' service.
    """

    SERVICE_MANUFACTURER = 'UPnP'
    SERVICE_TYPE = 'urn:schemas-upnp-org:service:WLANConfiguration:1'

    SERVICE_DEFAULT_VARIABLES = {
        "AssociatedDeviceAuthenticationState": { "data_type": "boolean", "default": None, "allowed_list": None},
        "AssociatedDeviceIPAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "AssociatedDeviceMACAddress": { "data_type": "string", "default": None, "allowed_list": None},
        "AuthenticationServiceMode": { "data_type": "string", "default": None, "allowed_list": "['None', 'LinkAuthentication', 'RadiusClient']"},
        "AutoRateFallBackEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "BSSID": { "data_type": "string", "default": None, "allowed_list": None},
        "BasicAuthenticationMode": { "data_type": "string", "default": None, "allowed_list": "['None', 'EAPAuthentication']"},
        "BasicDataTransmissionRates": { "data_type": "string", "default": None, "allowed_list": None},
        "BasicEncryptionModes": { "data_type": "string", "default": None, "allowed_list": "['None', 'WEPEncryption']"},
        "BeaconAdvertisementEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "BeaconType": { "data_type": "string", "default": None, "allowed_list": "['None', 'Basic', 'WPA', '11i', 'BasicandWPA', 'Basicand11i', 'WPAand11i', 'BasicandWPAand11i']"},
        "Channel": { "data_type": "ui1", "default": None, "allowed_list": None},
        "ChannelsInUse": { "data_type": "string", "default": None, "allowed_list": None},
        "DeviceOperationMode": { "data_type": "string", "default": None, "allowed_list": "['InfrastructureAccessPoint', 'WirelessBridgePointToPoint', 'WirelessBridgePointToMultipoint', 'WirelessRepeater', 'WirelessSTA']"},
        "DistanceFromRoot": { "data_type": "ui1", "default": None, "allowed_list": None},
        "IEEE11iAuthenticationMode": { "data_type": "string", "default": None, "allowed_list": "['TKIPAuthentication', 'EAPAuthentication', 'EAPandTKIPAuthentication']"},
        "IEEE11iEncryptionModes": { "data_type": "string", "default": None, "allowed_list": "['WEPEncryption', 'TKIPEncryption', 'WEPandTKIPEncryption', 'AESEncryption', 'WEPandAESEncryption', 'TKIPandAESEncryption', 'WEPandTKIPandAESEncryption']"},
        "InsecureOutOfBandAccessEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "KeyPassphrase": { "data_type": "string", "default": None, "allowed_list": None},
        "LocationDescription": { "data_type": "string", "default": None, "allowed_list": None},
        "OperationalDataTransmissionRates": { "data_type": "string", "default": None, "allowed_list": None},
        "PeerBSSID": { "data_type": "string", "default": None, "allowed_list": None},
        "PossibleChannels": { "data_type": "string", "default": None, "allowed_list": None},
        "PossibleDataTransmissionRates": { "data_type": "string", "default": None, "allowed_list": None},
        "PreSharedKey": { "data_type": "string", "default": None, "allowed_list": None},
        "PreSharedKeyIndex": { "data_type": "ui1", "default": None, "allowed_list": None},
        "RadioEnabled": { "data_type": "boolean", "default": None, "allowed_list": None},
        "RegulatoryDomain": { "data_type": "string", "default": None, "allowed_list": None},
        "SSID": { "data_type": "string", "default": None, "allowed_list": None},
        "TotalBytesReceived": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TotalBytesSent": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TotalIntegrityFailures": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TotalPSKFailures": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TotalPacketsReceived": { "data_type": "ui4", "default": None, "allowed_list": None},
        "TotalPacketsSent": { "data_type": "ui4", "default": None, "allowed_list": None},
        "WEPEncryptionLevel": { "data_type": "string", "default": None, "allowed_list": "['Disabled', '40-bit', '104-bit']"},
        "WEPKey": { "data_type": "string", "default": None, "allowed_list": None},
        "WEPKeyIndex": { "data_type": "ui1", "default": None, "allowed_list": None},
        "WPAAuthenticationMode": { "data_type": "string", "default": None, "allowed_list": "['PSKAuthentication', 'EAPAuthentication']"},
        "WPAEncryptionModes": { "data_type": "string", "default": None, "allowed_list": "['WEPEncryption', 'TKIPEncryption', 'WEPandTKIPEncryption', 'AESEncryption', 'WEPandAESEncryption', 'TKIPandAESEncryption', 'WEPandTKIPandAESEncryption']"},
    }

    SERVICE_EVENT_VARIABLES = {
        "TotalAssociations": { "data_type": "ui2", "default": None, "allowed_list": None},
    }

    def action_FactoryDefaultReset(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the FactoryDefaultReset action.
        """
        arguments = { }

        self.call_action("FactoryDefaultReset", arguments=arguments, aspects=aspects)

        return

    def action_Get11iBeaconSecurityProperties(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Get11iBeaconSecurityProperties action.

            :returns: "NewIEEE11iEncryptionModes", "NewIEEE11iAuthenticationMode"
        """
        arguments = { }

        out_params = self.call_action("Get11iBeaconSecurityProperties", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewIEEE11iEncryptionModes", "NewIEEE11iAuthenticationMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAuthenticationServiceMode(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAuthenticationServiceMode action.

            :returns: "NewAuthenticationServiceMode"
        """
        arguments = { }

        out_params = self.call_action("GetAuthenticationServiceMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAuthenticationServiceMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetAutoRateFallBackMode(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetAutoRateFallBackMode action.

            :returns: "NewAutoRateFallBackEnabled"
        """
        arguments = { }

        out_params = self.call_action("GetAutoRateFallBackMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAutoRateFallBackEnabled",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBSSID(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBSSID action.

            :returns: "NewBSSID"
        """
        arguments = { }

        out_params = self.call_action("GetBSSID", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewBSSID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBasicBeaconSecurityProperties(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBasicBeaconSecurityProperties action.

            :returns: "NewBasicEncryptionModes", "NewBasicAuthenticationMode"
        """
        arguments = { }

        out_params = self.call_action("GetBasicBeaconSecurityProperties", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewBasicEncryptionModes", "NewBasicAuthenticationMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBeaconAdvertisement(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBeaconAdvertisement action.

            :returns: "NewBeaconAdvertisementEnabled"
        """
        arguments = { }

        out_params = self.call_action("GetBeaconAdvertisement", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewBeaconAdvertisementEnabled",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetBeaconType(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetBeaconType action.

            :returns: "NewBeaconType"
        """
        arguments = { }

        out_params = self.call_action("GetBeaconType", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewBeaconType",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetByteStatistics(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetByteStatistics action.

            :returns: "NewTotalBytesSent", "NewTotalBytesReceived"
        """
        arguments = { }

        out_params = self.call_action("GetByteStatistics", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalBytesSent", "NewTotalBytesReceived",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetChannelInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetChannelInfo action.

            :returns: "NewChannel", "NewPossibleChannels"
        """
        arguments = { }

        out_params = self.call_action("GetChannelInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewChannel", "NewPossibleChannels",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetChannelsInUse(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetChannelsInUse action.

            :returns: "NewChannelsInUse"
        """
        arguments = { }

        out_params = self.call_action("GetChannelsInUse", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewChannelsInUse",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDataTransmissionRateInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDataTransmissionRateInfo action.

            :returns: "NewBasicDataTransmissionRates", "NewOperationalDataTransmissionRates", "NewPossibleDataTransmissionRates"
        """
        arguments = { }

        out_params = self.call_action("GetDataTransmissionRateInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewBasicDataTransmissionRates", "NewOperationalDataTransmissionRates", "NewPossibleDataTransmissionRates",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDefaultWEPKeyIndex(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDefaultWEPKeyIndex action.

            :returns: "NewDefaultWEPKeyIndex"
        """
        arguments = { }

        out_params = self.call_action("GetDefaultWEPKeyIndex", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDefaultWEPKeyIndex",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetDeviceOperationMode(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetDeviceOperationMode action.

            :returns: "NewDeviceOperationMode", "NewSSID", "NewBSSID", "NewChannel", "NewBasicDataTransmissionRates", "NewOperationalDataTransmissionRates", "NewDistanceFromRoot"
        """
        arguments = { }

        out_params = self.call_action("GetDeviceOperationMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewDeviceOperationMode", "NewSSID", "NewBSSID", "NewChannel", "NewBasicDataTransmissionRates", "NewOperationalDataTransmissionRates", "NewDistanceFromRoot",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetFailureStatusInfo(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetFailureStatusInfo action.

            :returns: "NewTotalIntegrityFailures", "NewTotalPSKFailures"
        """
        arguments = { }

        out_params = self.call_action("GetFailureStatusInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalIntegrityFailures", "NewTotalPSKFailures",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetGenericAssociatedDeviceInfo(self, NewAssociatedDeviceIndex, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetGenericAssociatedDeviceInfo action.

            :returns: "NewAssociatedDeviceMACAddress", "NewAssociatedDeviceIPAddress", "NewAssociatedDeviceAuthenticationState"
        """
        arguments = {
            "NewAssociatedDeviceIndex": NewAssociatedDeviceIndex,
        }

        out_params = self.call_action("GetGenericAssociatedDeviceInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAssociatedDeviceMACAddress", "NewAssociatedDeviceIPAddress", "NewAssociatedDeviceAuthenticationState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetInsecureOutOfBandAccessMode(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetInsecureOutOfBandAccessMode action.

            :returns: "NewInsecureOutOfBandAccessEnabled"
        """
        arguments = { }

        out_params = self.call_action("GetInsecureOutOfBandAccessMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewInsecureOutOfBandAccessEnabled",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetLocationDescription(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetLocationDescription action.

            :returns: "NewLocationDescription"
        """
        arguments = { }

        out_params = self.call_action("GetLocationDescription", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewLocationDescription",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPacketStatistics(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPacketStatistics action.

            :returns: "NewTotalPacketsSent", "NewTotalPacketsReceived"
        """
        arguments = { }

        out_params = self.call_action("GetPacketStatistics", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalPacketsSent", "NewTotalPacketsReceived",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetPreSharedKey(self, NewPreSharedKeyIndex, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetPreSharedKey action.

            :returns: "NewPreSharedKey", "NewPSKPassphrase"
        """
        arguments = {
            "NewPreSharedKeyIndex": NewPreSharedKeyIndex,
        }

        out_params = self.call_action("GetPreSharedKey", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewPreSharedKey", "NewPSKPassphrase",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRadioMode(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRadioMode action.

            :returns: "NewRadioEnabled"
        """
        arguments = { }

        out_params = self.call_action("GetRadioMode", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewRadioEnabled",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetRegulatoryDomain(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetRegulatoryDomain action.

            :returns: "NewRegulatoryDomain"
        """
        arguments = { }

        out_params = self.call_action("GetRegulatoryDomain", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewRegulatoryDomain",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSSID(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSSID action.

            :returns: "NewSSID"
        """
        arguments = { }

        out_params = self.call_action("GetSSID", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewSSID",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSecurityKeys(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSecurityKeys action.

            :returns: "NewWEPKey0", "NewWEPKey1", "NewWEPKey2", "NewWEPKey3", "NewPreSharedKey", "NewKeyPassphrase"
        """
        arguments = { }

        out_params = self.call_action("GetSecurityKeys", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewWEPKey0", "NewWEPKey1", "NewWEPKey2", "NewWEPKey3", "NewPreSharedKey", "NewKeyPassphrase",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetSpecificAssociatedDeviceInfo(self, NewAssociatedDeviceMACAddress, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetSpecificAssociatedDeviceInfo action.

            :returns: "NewAssociatedDeviceIPAddress", "NewAssociatedDeviceAuthenticationState"
        """
        arguments = {
            "NewAssociatedDeviceMACAddress": NewAssociatedDeviceMACAddress,
        }

        out_params = self.call_action("GetSpecificAssociatedDeviceInfo", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewAssociatedDeviceIPAddress", "NewAssociatedDeviceAuthenticationState",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetTotalAssociations(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetTotalAssociations action.

            :returns: "NewTotalAssociations"
        """
        arguments = { }

        out_params = self.call_action("GetTotalAssociations", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewTotalAssociations",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_GetWPABeaconSecurityProperties(self, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the GetWPABeaconSecurityProperties action.

            :returns: "NewWPAEncryptionModes", "NewWPAAuthenticationMode"
        """
        arguments = { }

        out_params = self.call_action("GetWPABeaconSecurityProperties", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in ("NewWPAEncryptionModes", "NewWPAAuthenticationMode",)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args

    def action_ResetAuthentication(self, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the ResetAuthentication action.
        """
        arguments = { }

        self.call_action("ResetAuthentication", arguments=arguments, aspects=aspects)

        return

    def action_Set11iBeaconSecurityProperties(self, NewIEEE11iEncryptionModes, NewIEEE11iAuthenticationMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the Set11iBeaconSecurityProperties action.
        """
        arguments = {
            "NewIEEE11iEncryptionModes": NewIEEE11iEncryptionModes,
            "NewIEEE11iAuthenticationMode": NewIEEE11iAuthenticationMode,
        }

        self.call_action("Set11iBeaconSecurityProperties", arguments=arguments, aspects=aspects)

        return

    def action_SetAuthenticationServiceMode(self, NewAuthenticationServiceMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAuthenticationServiceMode action.
        """
        arguments = {
            "NewAuthenticationServiceMode": NewAuthenticationServiceMode,
        }

        self.call_action("SetAuthenticationServiceMode", arguments=arguments, aspects=aspects)

        return

    def action_SetAutoRateFallBackMode(self, NewAutoRateFallBackEnabled, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetAutoRateFallBackMode action.
        """
        arguments = {
            "NewAutoRateFallBackEnabled": NewAutoRateFallBackEnabled,
        }

        self.call_action("SetAutoRateFallBackMode", arguments=arguments, aspects=aspects)

        return

    def action_SetBasicBeaconSecurityProperties(self, NewBasicEncryptionModes, NewBasicAuthenticationMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetBasicBeaconSecurityProperties action.
        """
        arguments = {
            "NewBasicEncryptionModes": NewBasicEncryptionModes,
            "NewBasicAuthenticationMode": NewBasicAuthenticationMode,
        }

        self.call_action("SetBasicBeaconSecurityProperties", arguments=arguments, aspects=aspects)

        return

    def action_SetBeaconAdvertisement(self, NewBeaconAdvertisementEnabled, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetBeaconAdvertisement action.
        """
        arguments = {
            "NewBeaconAdvertisementEnabled": NewBeaconAdvertisementEnabled,
        }

        self.call_action("SetBeaconAdvertisement", arguments=arguments, aspects=aspects)

        return

    def action_SetBeaconType(self, NewBeaconType, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetBeaconType action.
        """
        arguments = {
            "NewBeaconType": NewBeaconType,
        }

        self.call_action("SetBeaconType", arguments=arguments, aspects=aspects)

        return

    def action_SetChannel(self, NewChannel, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetChannel action.
        """
        arguments = {
            "NewChannel": NewChannel,
        }

        self.call_action("SetChannel", arguments=arguments, aspects=aspects)

        return

    def action_SetDataTransmissionRates(self, NewBasicDataTransmissionRates, NewOperationalDataTransmissionRates, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDataTransmissionRates action.
        """
        arguments = {
            "NewBasicDataTransmissionRates": NewBasicDataTransmissionRates,
            "NewOperationalDataTransmissionRates": NewOperationalDataTransmissionRates,
        }

        self.call_action("SetDataTransmissionRates", arguments=arguments, aspects=aspects)

        return

    def action_SetDefaultWEPKeyIndex(self, NewDefaultWEPKeyIndex, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDefaultWEPKeyIndex action.
        """
        arguments = {
            "NewDefaultWEPKeyIndex": NewDefaultWEPKeyIndex,
        }

        self.call_action("SetDefaultWEPKeyIndex", arguments=arguments, aspects=aspects)

        return

    def action_SetDeviceOperationMode(self, NewDeviceOperationMode, NewSSID, NewBSSID, NewChannel, NewBasicDataTransmissionRates, NewOperationalDataTransmissionRates, NewDistanceFromRoot, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetDeviceOperationMode action.
        """
        arguments = {
            "NewDeviceOperationMode": NewDeviceOperationMode,
            "NewSSID": NewSSID,
            "NewBSSID": NewBSSID,
            "NewChannel": NewChannel,
            "NewBasicDataTransmissionRates": NewBasicDataTransmissionRates,
            "NewOperationalDataTransmissionRates": NewOperationalDataTransmissionRates,
            "NewDistanceFromRoot": NewDistanceFromRoot,
        }

        self.call_action("SetDeviceOperationMode", arguments=arguments, aspects=aspects)

        return

    def action_SetInsecureOutOfBandAccessMode(self, NewInsecureOutOfBandAccessEnabled, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetInsecureOutOfBandAccessMode action.
        """
        arguments = {
            "NewInsecureOutOfBandAccessEnabled": NewInsecureOutOfBandAccessEnabled,
        }

        self.call_action("SetInsecureOutOfBandAccessMode", arguments=arguments, aspects=aspects)

        return

    def action_SetLocationDescription(self, NewLocationDescription, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetLocationDescription action.
        """
        arguments = {
            "NewLocationDescription": NewLocationDescription,
        }

        self.call_action("SetLocationDescription", arguments=arguments, aspects=aspects)

        return

    def action_SetPreSharedKey(self, NewPreSharedKeyIndex, NewPreSharedKey, NewPSKPassphrase, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetPreSharedKey action.
        """
        arguments = {
            "NewPreSharedKeyIndex": NewPreSharedKeyIndex,
            "NewPreSharedKey": NewPreSharedKey,
            "NewPSKPassphrase": NewPSKPassphrase,
        }

        self.call_action("SetPreSharedKey", arguments=arguments, aspects=aspects)

        return

    def action_SetRadioMode(self, NewRadioEnabled, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRadioMode action.
        """
        arguments = {
            "NewRadioEnabled": NewRadioEnabled,
        }

        self.call_action("SetRadioMode", arguments=arguments, aspects=aspects)

        return

    def action_SetRegulatoryDomain(self, NewRegulatoryDomain, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetRegulatoryDomain action.
        """
        arguments = {
            "NewRegulatoryDomain": NewRegulatoryDomain,
        }

        self.call_action("SetRegulatoryDomain", arguments=arguments, aspects=aspects)

        return

    def action_SetSSID(self, NewSSID, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetSSID action.
        """
        arguments = {
            "NewSSID": NewSSID,
        }

        self.call_action("SetSSID", arguments=arguments, aspects=aspects)

        return

    def action_SetSecurityKeys(self, NewWEPKey0, NewWEPKey1, NewWEPKey2, NewWEPKey3, NewPreSharedKey, NewKeyPassphrase, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetSecurityKeys action.
        """
        arguments = {
            "NewWEPKey0": NewWEPKey0,
            "NewWEPKey1": NewWEPKey1,
            "NewWEPKey2": NewWEPKey2,
            "NewWEPKey3": NewWEPKey3,
            "NewPreSharedKey": NewPreSharedKey,
            "NewKeyPassphrase": NewKeyPassphrase,
        }

        self.call_action("SetSecurityKeys", arguments=arguments, aspects=aspects)

        return

    def action_SetWPABeaconSecurityProperties(self, NewWPAEncryptionModes, NewWPAAuthenticationMode, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        """
            Calls the SetWPABeaconSecurityProperties action.
        """
        arguments = {
            "NewWPAEncryptionModes": NewWPAEncryptionModes,
            "NewWPAAuthenticationMode": NewWPAAuthenticationMode,
        }

        self.call_action("SetWPABeaconSecurityProperties", arguments=arguments, aspects=aspects)

        return
