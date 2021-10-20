"""
.. module:: landscapedescription
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`TestLandscape` class and associated diagnostic.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


import os
import yaml

from akit.exceptions import AKitConfigurationError
from akit.environment.context import Context
from akit.xlogging.foundations import getAutomatonKitLogger

from akit.integration.clients.linuxclientintegration import LinuxClientIntegration
from akit.integration.clients.windowsclientintegration import WindowsClientIntegration
from akit.integration.cluster.clusterintegration import ClusterIntegration
from akit.integration.credentials.sshcredential import SshCredential

# Declare a literal UpnpFacotry type for use with typing
# to allow for typing without creating circular reference
LITERAL_LANDSCAPE_TYPE = 'akit.integration.landscaping.landscape.Landscape'

class LandscapeDescription:
    """
        The base class for all derived :class:`LandscapeDescription` objects.  The
        :class:`LandscapeDescription` is used to load a description of the entities
        and resources in the tests landscape that will be used by the tests.
    """

    @classmethod
    def register_integration_points(cls, landscape: LITERAL_LANDSCAPE_TYPE):
        """
            Method called during the test framework ininitalization in order to register integartion couplings and their
            associated roles with the test framework.

            :param landscape: A reference to the landscape singleton object.  We pass in the landscape parameter in order
                              to eliminate the need to import the landscape module which would cause a circular reference.
        """
        landscape.register_integration_point("primary-linux", LinuxClientIntegration)
        landscape.register_integration_point("secondary-linux", LinuxClientIntegration)

        landscape.register_integration_point("primary-windows", WindowsClientIntegration)
        landscape.register_integration_point("secondary-windows", WindowsClientIntegration)

        landscape.register_integration_point("primary-cluster", ClusterIntegration)
        landscape.register_integration_point("secondary-cluster", ClusterIntegration)
        return

    def load(self, landscape_file: str):
        """
            Loads and validates the landscape description file.
        """
        logger = getAutomatonKitLogger()

        landscape_info = None

        with open(landscape_file, 'r') as lf:
            lfcontent = lf.read()
            landscape_info = yaml.safe_load(lfcontent)

        errors, warnings = self.validate_landscape(landscape_info)

        if len(errors) > 0:
            errmsg_lines = [
                "ERROR Landscape validation failures:"
            ]
            for err in errors:
                errmsg_lines.append("    %s" % err)

            errmsg = os.linesep.join(errmsg_lines)
            raise AKitConfigurationError(errmsg) from None

        if len(warnings) > 0:
            for wrn in warnings:
                logger.warn("Landscape Configuration Warning: (%s)" % wrn)

        if "devices" in landscape_info["pod"]:
            devices = landscape_info["pod"]["devices"]

            device_lookup_table = {}
            for dev in devices:
                dev_type = dev["deviceType"]
                if dev_type == "network/upnp":
                    dkey = "UPNP:{}".format(dev["upnp"]["USN"]).upper()
                    device_lookup_table[dkey] = dev
                elif dev_type == "network/ssh":
                    dkey = "SSH:{}".format(dev["host"]).upper()
                    device_lookup_table[dkey] = dev

            ctx = Context()
            conf = ctx.lookup("/environment/configuration")

            skip_devices_override = conf["skip-devices-override"]
            for dev_key in skip_devices_override:
                dev_key = dev_key.upper()
                if dev_key in device_lookup_table:
                    device = device_lookup_table[dev_key]
                    device["skip"] = True

        return landscape_info

    def validate_landscape(self, landscape_info):
        """
            Validates the landscape description file.
        """
        errors = []
        warnings = []

        if "pod" in landscape_info:
            podinfo = landscape_info["pod"]
            if "devices" in podinfo:
                devices_list = podinfo["devices"]
                child_errors, child_warnings = self.validate_devices_list(devices_list, prefix="")
                errors.extend(child_errors)
                warnings.extend(child_warnings)
            elif "environment" in podinfo:
                envinfo = landscape_info["environment"]
                child_errors, child_warnings = self.validate_environment(envinfo)
                errors.extend(child_errors)
                warnings.extend(child_warnings)
            else:
                errors.append(["/pod/devices", "A pod description requires a 'devices' list data member."])
        else:
            errors.append(["/pod", "A landscape description requires a 'pod' data member."])

        return errors, warnings

    def validate_devices_list(self, devlist, prefix=""): # pylint: disable=unused-argument
        """
            Verifies that all the devices in a device list are valid and returns a list of errors found.
        """
        errors = []
        warnings = []

        for devidx, devinfo in enumerate(devlist):
            item_prefix = "/devices[%d]" % devidx
            child_errors, child_warnings = self.validate_device_info(devinfo, prefix=item_prefix)
            errors.extend(child_errors)
            warnings.extend(child_warnings)

        return errors, warnings

    def validate_device_info(self, devinfo, prefix=""):
        """
            Verifies that a device info dictionary has the required common fields and also has valid
            information for the declared device type.  Returns a list of errors found.

            Required Common Fields:
                deviceType

            Valid Device Types:
                network/ssh
                network/upnp
        """
        errors = []
        warnings = []

        if "deviceType" in devinfo:
            deviceType = devinfo["deviceType"]
            if deviceType == "network/upnp":
                if "upnp" in devinfo:
                    upnpinfo = devinfo["upnp"]
                    child_errors, child_warnings = self.validate_upnp_info(upnpinfo, prefix=prefix + "/upnp")
                    errors.extend(child_errors)
                    warnings.extend(child_warnings)
                else:
                    errors.append(prefix + "upnp", "Device type 'network/upnp' must have a 'upnp' data member.")
            if deviceType == "network/ssh":
                if "host" not in devinfo:
                    errors.append("SSH Devices must have a 'host' field.")
                if "credentials" not in devinfo:
                    errors.append("Device type 'network/ssh' must have a 'credentials' data member.")
        else:
            errors.append(prefix + "deviceType", "Device information is missing the required 'deviceType' data member.")

        return errors, warnings

    def validate_environment(self, envinfo):
        """
        "environment":
            "label": "production"
            

            "credentials":
            -   "identifier": "power"
                "category": "basic"
                "username": "admin"
                "password": "Acess2Power!!"

            -   "identifier": "casey-node"
                "category": "ssh"
                "username": "ubuntu"
                "password": "Skate4Fun@@"
                "keyfile": "~/.ssh/id_casey_rsa"

            -   "identifier": "player-ssh"
                "category": "ssh"
                "username": "root"
                "password": "iLpAvzuFezru"

            -   "identifier": "player-muse"
                "category": "muse"
                "username": "myron.sonos@gmail.com"
                "password": "Acess2Play"
                "apikey": "f71f269e-0b9f-4f73-9c13-4efccd2ce77e"
                "secret": "bdfeabf8-3fb1-47ea-9789-fd6c58cd019d"

        """
        errors = []
        warnings = []

        if "credentials" in envinfo:
            cred_list = envinfo["credentials"]
            child_errors, child_warnings = self.validate_environment_credentials(cred_list)
            errors.extend(child_errors)
            warnings.extend(child_warnings)
        elif "muse" in envinfo:
            muse_info = envinfo["muse"]
            child_errors, child_warnings = self.validate_environment_muse(muse_info)
            errors.extend(child_errors)
            warnings.extend(child_warnings)
        elif "networking" in envinfo:
            net_info = envinfo["networking"]
            child_errors, child_warnings = self.validate_environment_networking(net_info)
            errors.extend(child_errors)
            warnings.extend(child_warnings)

        return errors, warnings

    def validate_environment_credentials(self, cred_list):
        errors = []
        warnings = []

        identifier_set = set()

        for cinfo in cred_list:
            if "identifier" in cinfo:
                identifier = cinfo["identifier"]
                if identifier in identifier_set:
                    errmsg = "Duplicate identifer found. identifier=%s" % identifier
                    errors.append(errmsg)
                else:
                    identifier_set.add(identifier)
            else:
                errmsg = "All credentials must have an identifier field. cinfo=%r" % cinfo
                errors.append(errmsg)

            if "category" in cinfo:
                category = cinfo["category"]
                if category == "basic":
                    child_errors, child_warnings =  self.validate_environment_cred_basic(cinfo)
                    errors.extend(child_errors)
                    warnings.extend(child_warnings)
                elif category == "ssh":
                    child_errors, child_warnings =  self.validate_environment_cred_ssh(cinfo)
                    errors.extend(child_errors)
                    warnings.extend(child_warnings)
                else:
                    warnmsg = "Unknown credential category=%s. info=%r" % (category, cinfo)
                    warnings.append(warnmsg)
            else:
                errmsg = "Credential info has no category. info=%r" % cinfo
                errors.append(errmsg)

        return errors, warnings

    def validate_environment_cred_basic(self, cred):
        """
            Validates the non-common fields of a 'basic' credential.
        """
        errors = []
        warnings = []

        if "username" in cred:
            if len(cred["username"].strip()) == 0:
                errmsg = "The 'username' for a basic credential cannot be empty."
                errors.append(errmsg)
        else:
            errmsg = "Basic credentials must have a 'username' field."
            errors.append(errmsg)

        if "password" not in cred:
            errmsg = "Basic credentials must have a 'password' field."
            errors.append(errmsg)

        return errors, warnings

    def validate_environment_cred_ssh(self, cred):
        """
            Validates the non-common fields of an 'ssh' credential.
        """
        """
        -   "identifier": "casey-node"
            "category": "ssh"
            "username": "ubuntu"
            "password": "Skate4Fun@@"
            "keyfile": "~/.ssh/id_casey_rsa"

        """
        errors = []
        warnings = []

        if "username" in cred:
            if len(cred["username"].strip()) == 0:
                errmsg = "The 'username' for an SSH credential cannot be empty."
                errors.append(errmsg)
        else:
            errmsg = "SSH credentials must have a 'username' field."
            errors.append(errmsg)

        if "password" not in cred and "keyfile" not in cred:
            errmsg = "SSH credentials must have a 'password' or 'keyfile' field."
            errors.append(errmsg)
        elif "keyfile" in cred:
            keyfile = os.path.abspath(os.path.expanduser(os.path.expandvars(cred["keyfile"])))
            if not os.path.exists(keyfile):
                errmsg = "The specified SSH keyfile does not exist. file=%s" % keyfile
                errors.append(errmsg)

        return errors, warnings

    def validate_environment_muse(self, muse_info):
        """
            "muse":
                "authhost": "oauth.ws.sonos.com"
                "ctlhost": "api.ws.sonos.com"
                "version": "v3"
        """
        errors = []
        warnings = []

        # TODO: Note this is a No-op for now because muse is not fully implemented

        return errors, warnings

    def validate_environment_networking(self, net_info):
        """
        """
        errors = []
        warnings = []

        if "upnp" in net_info:
            upnp = net_info["upnp"]
            if isinstance(upnp, dict):
                for fkey in upnp:
                    if fkey == "exclude_interfaces":
                        continue
                    else:
                        warnmsg = "Unknown field (%s) found in environment/networking/upnp" % fkey
                        warnings.append(warnmsg)
            else:
                errmsg = "Field environment/networking/upnp should be a dictionary field."
                errors.append(errmsg)

        return errors, warnings

    def validate_upnp_info(self, upnpinfo, prefix=""): # pylint: disable=no-self-use,unused-argument
        """
            Verifies that a upnp info dictionary has valid data member combinations and can be used. Returns a
            list of errors found.
        """
        errors = []
        warnings = []

        if "USN" not in upnpinfo:
            errors.append(prefix + "USN", "UPnP information is missing a 'USN' data member.")
        if "modelNumber" not in upnpinfo:
            errors.append(prefix + "modelNumber", "UPnP information is missing a 'modelNumber' data member.")
        if "modelName" not in upnpinfo:
            errors.append(prefix + "modelName", "UPnP information is missing a 'modelName' data member.")

        return errors, warnings
