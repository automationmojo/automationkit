"""
.. module:: landscapedescription
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`LandscapeDescription` class.

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

from typing import Optional, TYPE_CHECKING

import copy
import json
import os
import shutil
import traceback
import yaml

from akit.environment.contextpaths import ContextPaths

from akit.exceptions import AKitConfigurationError, AKitRuntimeError
from akit.environment.context import Context
from akit.xlogging.foundations import getAutomatonKitLogger

if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

class LandscapeDescription:
    """
        The base class for all derived :class:`LandscapeDescription` objects.  The
        :class:`LandscapeDescription` is used to load a description of the entities
        and resources in the tests landscape that will be used by the tests.
    """

    @classmethod
    def register_integration_points(cls, landscape: "Landscape"):
        """
            Method called during the test framework ininitalization in order to register integartion couplings and their
            associated roles with the test framework.

            :param landscape: A reference to the landscape singleton object.  We pass in the landscape parameter in order
                              to eliminate the need to import the landscape module which would cause a circular reference.
        """
        return

    def load(self, landscape_file: str, log_to_directory: Optional[str]=None):
        """
            Loads and validates the landscape description file.
        """
        logger = getAutomatonKitLogger()

        landscape_info = None

        with open(landscape_file, 'r') as lf:
            lfcontent = lf.read()
            landscape_info = yaml.safe_load(lfcontent)

        if log_to_directory is not None:
            try:
                landscape_file_basename = os.path.basename(landscape_file)
                landscape_file_basename, landscape_file_ext = os.path.splitext(landscape_file_basename)

                landscape_file_copy = os.path.join(log_to_directory, "landscape-declared{}".format(landscape_file_ext))
                shutil.copy2(landscape_file, landscape_file_copy)

                # Create a json copy of the landscape file until the time when we can
                # parse yaml in the test summary javascript.
                landscape_info_copy = copy.deepcopy(landscape_info)

                landscape_file_copy = os.path.join(log_to_directory, "landscape-declared.json")
                with open(landscape_file_copy, 'w') as lsf:
                    json.dump(landscape_info_copy, lsf, indent=4)
            except Exception as xcpt:
                err_msg = "Error while logging the landscape file (%s)%s%s" % (
                    landscape_file, os.linesep, traceback.format_exc())
                raise AKitRuntimeError(err_msg) from xcpt

        errors, warnings = self.validate_landscape(landscape_info)

        if len(errors) > 0:
            errmsg_lines = [
                "ERROR Landscape validation failures:"
            ]
            for err_path, err_msg in errors:
                errmsg_lines.append("    {}: {}".format(err_path, err_msg))

            errmsg = os.linesep.join(errmsg_lines)
            raise AKitConfigurationError(errmsg) from None

        if len(warnings) > 0:
            for wrn_path, wrn_msg in warnings:
                logger.warn("Landscape Configuration Warning: ({}) {}".format(wrn_path, wrn_msg))

        if "devices" in landscape_info["pod"]:
            devices = landscape_info["pod"]["devices"]

            device_lookup_table = {}
            for dev in devices:
                dev_type = dev["deviceType"]
                if dev_type == "network/upnp":
                    upnp_info = dev["upnp"]
                    dkey = None
                    if "hint" in upnp_info:
                        dkey = upnp_info["hint"]
                    elif "USN" in upnp_info:
                        dkey = upnp_info["USN"]
                    dkey = "UPNP:{}".format(dkey.upper())
                    device_lookup_table[dkey] = dev
                elif dev_type == "network/ssh":
                    dkey = "SSH:{}".format(dev["host"]).upper()
                    device_lookup_table[dkey] = dev

            ctx = Context()
            skipped_devices = ctx.lookup(ContextPaths.SKIPPED_DEVICES, default=[])

            for dev_key in skipped_devices:
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
        """
        errors = []
        warnings = []

        return errors, warnings

    def validate_upnp_info(self, upnpinfo, prefix=""): # pylint: disable=no-self-use,unused-argument
        """
            Verifies that a upnp info dictionary has valid data member combinations and can be used. Returns a
            list of errors found.
        """
        errors = []
        warnings = []

        if "hint" not in upnpinfo:
            if "USN" not in upnpinfo:
                errors.append((prefix + "USN", "UPnP information is missing a 'hint' or 'USN' data member."))
            else:
                warnings.append((prefix + "USN", "UPnP information 'USN' field has been replaced by the 'hint' field."))

        if "modelNumber" not in upnpinfo:
            errors.append((prefix + "modelNumber", "UPnP information is missing a 'modelNumber' data member."))
        if "modelName" not in upnpinfo:
            errors.append((prefix + "modelName", "UPnP information is missing a 'modelName' data member."))

        return errors, warnings
