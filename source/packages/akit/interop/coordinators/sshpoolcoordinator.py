"""
.. module:: sshpoolcoordinator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the SshPoolCoordinator which is used for managing connectivity with pools of ssh capable devices

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

from typing import List, Optional, Union, TYPE_CHECKING

import os
import pprint
import socket
import weakref

from akit.exceptions import AKitConfigurationError
from akit.friendlyidentifier import FriendlyIdentifier

from akit.interop.coordinators.coordinatorbase import CoordinatorBase
from akit.interop.coordinators.upnpcoordinator import UpnpCoordinator

from akit.interop.landscaping.landscapedevice import LandscapeDevice

from akit.interop.agents.sshagent import SshAgent

if TYPE_CHECKING:
    from akit.interop.landscaping.landscape import Landscape

def format_ssh_device_configuration_error(message, sshdev_config):
    """
        Takes an error message and an SSH device configuration info dictionary and
        formats a configuration error message.
    """
    error_lines = [
        message,
        "DEVICE:"
    ]

    dev_repr_lines = pprint.pformat(sshdev_config, indent=4).splitlines(False)
    for dline in dev_repr_lines:
        error_lines.append("    " + dline)
    
    errmsg = os.linesep.join(error_lines)
    return errmsg

class SshPoolCoordinator(CoordinatorBase):
    """
        The :class:`SshPoolCoordinator` creates a pool of agents that can be used to
        coordinate the interop activities of the automation process and remote SSH
        nodes.
    """
    # pylint: disable=attribute-defined-outside-init

    def __init__(self, lscape: "Landscape", *args, **kwargs):
        super(SshPoolCoordinator, self).__init__(lscape, *args, **kwargs)
        return

    def _initialize(self, *_args, **_kwargs):
        """
            Called by the CoordinatorBase constructor to perform the one time initialization of the coordinator Singleton
            of a given type.
        """
        # pylint: disable=arguments-differ
        self._cl_upnp_hint_to_ip_lookup = {}
        self._cl_ip_to_host_lookup = {}
        return

    def attach_to_devices(self, sshdevices: List[LandscapeDevice], upnp_coord: Optional[UpnpCoordinator]=None):
        """
            Processes a list of device configs and creates and registers devices and SSH device extensions
            attached with the landscape for the devices not already registered.  If a device has already
            been registered by the UPNP coordinator then a device extension is created and attached to the
            existing device.

            :param sshdevices: A list of ssh device configuration dictionaries.
            :param upnp_coord: The UpnpCoordinator singleton instance.
        """

        lscape = self.landscape

        ssh_config_errors = []

        ssh_devices_available = []
        ssh_devices_unavailable = []

        for sshdev in sshdevices:
            sshdev_config = sshdev.device_config
            ssh_credential_list = sshdev.ssh_credentials
            if len(ssh_credential_list) == 0:
                errmsg = format_ssh_device_configuration_error(
                        "All SSH devices must have at least one valid credential.", sshdev_config)
                raise AKitConfigurationError(errmsg) from None

            ssh_cred_by_role = {}
            for ssh_cred in ssh_credential_list:
                cred_role = ssh_cred.role
                if cred_role not in ssh_cred_by_role:
                    ssh_cred_by_role[cred_role] = ssh_cred
                else:
                    errmsg = format_ssh_device_configuration_error(
                        "The SSH device had more than one credentials with the role '{}'".format(cred_role), sshdev_config)
                    raise AKitConfigurationError(errmsg) from None

            if "priv" not in ssh_cred_by_role:
                errmsg = format_ssh_device_configuration_error(
                        "All SSH devices must have a 'priv' credential.", sshdev_config)
                raise AKitConfigurationError(errmsg) from None

            priv_cred = ssh_cred_by_role["priv"]

            dev_type = sshdev_config["deviceType"]

            host = None
            upnp_hint = None
            if "host" in sshdev_config:
                host = sshdev_config["host"]
            elif dev_type == "network/upnp":
                upnp_config = sshdev_config["upnp"]

                if "hint" in upnp_config:
                    upnp_hint = upnp_config["hint"]
                elif "USN" in upnp_config:
                    upnp_hint = upnp_config["USN"]
                if upnp_coord is not None:
                    upnp_dev = upnp_coord.lookup_device_by_upnp_hint(upnp_hint)
                    dev = upnp_dev.basedevice
                    if dev is not None:
                        ipaddr = upnp_dev.IPAddress
                        host = ipaddr
                        sshdev_config["host"] = host
                        self._cl_upnp_hint_to_ip_lookup[upnp_hint] = ipaddr
                else:
                    ssh_config_errors.append(sshdev_config)

            if host is not None:
                called_id = dev.identity
                ip = socket.gethostbyname(host)
                self._cl_ip_to_host_lookup[ip] = host

                agent = SshAgent(host, priv_cred, users=ssh_cred_by_role, called_id=called_id)

                sshdev_config["ipaddr"] = agent.ipaddr
                try:
                    status, stdout, stderr = agent.run_cmd("echo Hello")
                    if status == 0 and stdout.strip() == "Hello":
                        ssh_devices_available.append(sshdev_config)
                    else:
                        ssh_devices_unavailable.append(sshdev_config)
                except:
                    ssh_devices_unavailable.append(sshdev_config)

                self._cl_children[host] = agent

                coord_ref = weakref.ref(self)

                basedevice = None
                if upnp_hint is not None:
                    basedevice = lscape._internal_lookup_device_by_hint(upnp_hint) # pylint: disable=protected-access
                else:
                    fdid = FriendlyIdentifier(host, host)
                    basedevice = lscape._create_landscape_device(fdid, dev_type, sshdev_config)
                    basedevice = lscape._enhance_landscape_device(basedevice, agent)
                    basedevice.initialize_features()

                basedevice.attach_extension("ssh", agent)

                basedevice_ref = weakref.ref(basedevice)
                agent.initialize(coord_ref, basedevice_ref, host, ip, sshdev_config)

                # If this device does not have a USN or hint then it is not a UPNP device so the
                # SshPoolCoordinator is repsonsible for activating it
                if upnp_hint is None:
                    lscape._internal_activate_device(host)

            else:
                ssh_config_errors.append(sshdev_config)

        self._available_devices = ssh_devices_available
        self._unavailable_devices = ssh_devices_unavailable

        return ssh_config_errors, ssh_devices_available, ssh_devices_unavailable

    def lookup_device_by_host(self, host: str) -> Union[LandscapeDevice, None]:
        """
            Looks up the agent for a device by its hostname.  If the
            agent is not found then the API returns None.

            :param host: The host name of the LandscapeDevice to search for.

            :returns: The found LandscapeDevice or None
        """
        device = None

        self._coord_lock.acquire()
        try:
            if host in self._cl_children:
                device = self._cl_children[host].basedevice
        finally:
            self._coord_lock.release()

        return device

    def lookup_device_by_ip(self, ip) -> Union[LandscapeDevice, None]:
        """
            Looks up the agent for a device by its ip address.  If the
            agent is not found then the API returns None.

            :param ip: The ip address of the LandscapeDevice to search for.

            :returns: The found LandscapeDevice or None
        """
        device = None

        self._coord_lock.acquire()
        try:
            if ip in self._cl_ip_to_host_lookup:
                if ip in self._cl_ip_to_host_lookup:
                    host = self._cl_ip_to_host_lookup[ip]
                    if host in self._cl_children:
                        device = self._cl_children[host].basedevice
        finally:
            self._coord_lock.release()

        return device

    def verify_connectivity(self, cmd: str = "echo 'It Works'", user: Optional[str] = None, raiseerror: bool = True) -> List[tuple]:
        """
            Loops through the nodes in the SSH pool and utilizes the credentials for the specified user in order to verify
            connectivity with the remote node.

            :param cmd: A command to run on the remote machine in order
                        to verify that ssh connectivity can be establish.
            :param user: The name of the user credentials to use for connectivity.
                         If the 'user' parameter is not provided, then the
                         credentials of the default or priviledged user will be used.
            :param raiseerror: A boolean value indicating if this API should raise an Exception on failure.

            :returns: A list of errors encountered when verifying connectivity with the devices managed or watched by the coordinator.
        """
        results = []

        for agent in self.children_as_extension:
            host = agent.host
            ipaddr = agent.ipaddr
            try:
                status, stdout, stderr = agent.run_cmd(cmd)
                results.append((host, ipaddr, status, stdout, stderr, None))
            except Exception as xcpt: # pylint: disable=broad-except
                if raiseerror:
                    raise
                results.append((host, ipaddr, None, None, None, xcpt))

        return results
