"""
.. module:: sshagent
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`SshAgent` class and associated diagnostic.

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

from typing import Callable, Optional, Sequence, Union, Tuple
from types import TracebackType

import os
import re
import socket
import stat
import threading
import time
import weakref

from datetime import datetime, timedelta

from akit.aspects import ActionPattern, AspectsCmd, LoggingPattern, DEFAULT_CMD_ASPECTS
from akit.exceptions import AKitCommandError, AKitInvalidConfigError, AKitNotOverloadedError, AKitSemanticError, AKitTimeoutError
from akit.interfaces.icommandrunner import ICommandRunner
from akit.timeouts import TimeoutContext

from akit.xformatting import indent_lines, format_command_result
from akit.xlogging.foundations import getAutomatonKitLogger
from akit.xlogging.scopemonitoring import MonitoredScope

from akit.interop.credentials.sshcredential import SshCredential
from akit.interop.landscaping.landscapedeviceextension import LandscapeDeviceExtension

import paramiko

logger = getAutomatonKitLogger()

DEFAULT_SSH_TIMEOUT = 300
DEFAULT_SSH_RETRY_INTERVAL = .5

DEFAULT_FAILURE_LABEL = "Failure"
DEFAULT_SUCCESS_LABEL = "Success"

INTERACTIVE_PROMPT="PROMPT%:%:%"
INTERACTIVE_PROMPT_BYTES = INTERACTIVE_PROMPT.encode('utf-8')

TEMPLATE_COMMAND_FAILURE = "RUNCMD%s: {} running CMD=%s{}STDOUT:{}%s{}STDERR:{}%s".format(DEFAULT_FAILURE_LABEL, *([os.linesep] * 4))
TEMPLATE_COMMAND_SUCCESS = "RUNCMD%s: {} running CMD=%s{}STDOUT:{}%s{}STDERR:{}%s".format(DEFAULT_SUCCESS_LABEL, *([os.linesep] * 4))

#                    PERMS          LINKS   OWNER       GROUPS    SIZE   MONTH  DAY  TIME    NAME
#                  rwxrwxrwx         24      myron      myron     4096   Jul    4   00:37  PCBs
REGEX_DIRECTORY_ENTRY = re.compile(r"([\S]+)[\s]+([0-9]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([0-9]+)[\s]+([A-za-z]+[\s]+[0-9]+[\s]+[0-9:]+)[\s]+([\S\s]+)")
def lookup_entry_type(pdir: str, ename: str, finfo: paramiko.SFTPAttributes) -> str:
    """
        Determines the entry type labelto assign to a file entry based on the st_mode of the file information.

        :param pdir: The parent directory of the file, passed for logging purposes.
        :param ename: The entry name of the file in the directory listing.
        :param finfo: The file information as returned by lstat on the file entry.

        :returns: A label indicating the type of directory entry.
    """
    etype = None
    if stat.S_ISREG(finfo.st_mode):
        etype = "file"
    elif stat.S_ISDIR(finfo.st_mode):
        etype = "dir"
    elif stat.S_ISLNK(finfo.st_mode):
        etype = "link"
    elif stat.S_ISCHR(finfo.st_mode):
        etype = "char"
    elif stat.S_ISBLK(finfo.st_mode):
        etype = "block"
    else:
        print ("ERROR: Unknown entry type. pdir=%s, ename=%s" % (pdir, ename))

    return etype

def primitive_list_directory(ssh_client: paramiko.SSHClient, directory: str) -> dict:
    """
        Uses a primitive method to create a list of the files and folders in a directory
        by running the 'ls -al' commands on the directory.  This is required if the SSH
        server does not support sftp.

        :param ssh_client: A :class:`paramiko.SSHClient` object that has already been connected
                           to the remote server.
        :param directory: The remote directory to get a list catalog for.

        :returns: A dictionary with the information about the items in the target directory.
    """
    entries = None

    ls_cmd = "ls -al %s" % directory

    status, stdout, stderr = ssh_execute_command(ssh_client, ls_cmd)

    if status == 0:
        entries = primitive_parse_directory_listing(directory, stdout)
    else:
        # Allow permission denied errors
        if stderr.find("Permission denied") < 0:
            errmsg = "Error attempting to get a primitive directory listing.\n    CMD=%s\n    STDERR:\n%s" % (ls_cmd, stderr)
            raise Exception(errmsg)

    return entries

def primitive_list_tree(ssh_client: paramiko.SSHClient, treeroot: str, max_depth: int=1) -> dict:
    """
        Uses a primitive method to create an information tree about the files and folders
        in a directory tree by running 'ls -al' commands on the directory tree.  This is
        required if the SSH server does not support sftp.

        :param ssh_client: A :class:`paramiko.SSHClient` object that has already been connected
                           to the remote server.
        :param treeroot: The remote root directory to get a directory tree catalog for.
        :param max_depth: The maximum descent depth to go to when building the tree catalog.

        :returns: A dictionary with the information about the root directory and its children.
    """

    level_items = primitive_list_directory(ssh_client, treeroot)

    if max_depth > 1:
        if not treeroot.endswith("/"):
            treeroot = treeroot + "/"

        for nxtitem in level_items.values():
            nxtname = nxtitem["name"]
            if nxtitem["type"] == "dir":
                nxtroot = treeroot + nxtname
                nxtchildren = primitive_list_tree_recurse(ssh_client, nxtroot, max_depth - 1)
                nxtitem.update(nxtchildren)

    tree_info = {
        "name": treeroot,
        "items": level_items
    }

    return tree_info

def primitive_list_tree_recurse(ssh_client: paramiko.SSHClient, targetdir: str, remaining: int) -> dict:
    """
        Method which is called recursively to list the items in a directory and to form a tree
        of information about the files under a room directory.  This method utilizes primitive
        shell commands in order to get directory information and is used when the SSH server on a
        device does not support FTP based access or file queries

        :params ssh_client: A paramiko.SSHClient to use for running commands to discover the information
                            about a directory.
        :params targetdir: The target directory of the local tree to scan.
        :params remaining: The remaining levels to descend

        :returns: A dictionary with the information about the target directory and its children.
    """

    level_items = primitive_list_directory(ssh_client, targetdir)

    if remaining > 1:
        if not targetdir.endswith("/"):
            targetdir = targetdir + "/"

        for nxtitem in level_items.values():
            nxtname = nxtitem["name"]
            if nxtitem["type"] == "dir":
                nxttarget = targetdir + nxtname
                nxtchildren = primitive_list_tree_recurse(ssh_client, nxttarget, remaining - 1)
                nxtitem.update(nxtchildren)

    children_info = {
        "items": level_items
    }

    return children_info

def primitive_parse_directory_listing(listing_dir:str, content: str) -> dict:
    """
        Method which is called parse the information associated with a directory listing.

        :params listing_dir: The directory path associated with the directory listing content being parsed.
        :params content: The directory listing content to be parsed.

        :returns: A dictionary with the directory entry items from a directoy based on the directory listing content being parsed.
    """
    entries = {}

    listing_lines = content.splitlines(False)
    for nxtline in listing_lines:
        nxtline = nxtline.strip()

        mobj = REGEX_DIRECTORY_ENTRY.match(nxtline)
        if mobj is not None:
            mgroups = mobj.groups()

            name = mgroups[6]
            if name == "." or name == "..":
                continue

            perms = mgroups[0]

            perms_tc = perms[0]
            etype = None
            if perms_tc == '-':
                etype = "file"
            elif perms_tc == 'd':
                etype = "dir"
            elif perms_tc == 'l':
                etype = "link"
                name, _ = name.split(" -> ")
            elif perms_tc == 'c':
                etype = "char"
            elif perms_tc == 'b':
                etype = "block"
            else:
                raise Exception("Unknown directory listing entry type. dir=%s tc=%s" % (listing_dir, perms_tc))

            dentry = {
                "name": name,
                "perms": perms,
                "type": etype,
                "owner": mgroups[2],
                "group": mgroups[3],
                "size": mgroups[4],
                "modified": mgroups[5]
            }

            entries[name] = dentry

    return entries

def primitive_directory_exists(ssh_client: paramiko.SSHClient, remotedir: str) -> bool:
    """
        Checks to see if the specified file exists.

        :param ssh_client: A paramiko.SSHClient to run commands over.
        :param remotedir: The path of the remote directory to check for existance.

        :returns: A boolean indicating if the file exists.
    """
    exists = False

    existscmd = 'test -d {0} && echo exists'.format(remotedir)
    status, stdout, stderr = ssh_execute_command(ssh_client, existscmd)

    if status == 0:
        exists = stdout.strip() == 'exists'

    return exists

def primitive_file_exists(ssh_client: paramiko.SSHClient, remotepath: str) -> bool:
    """
        Checks to see if the specified file exists.

        :param ssh_client: A paramiko.SSHClient to run commands over.
        :param remotepath: The path of the remote file to check for existance.

        :returns: A boolean indicating if the file exists.
    """
    exists = False

    existscmd = 'test -f {0} && echo exists'.format(remotepath)
    status, stdout, stderr = ssh_execute_command(ssh_client, existscmd)

    if status == 0:
        exists = stdout.strip() == 'exists'

    return exists

def primitive_file_pull(ssh_client: paramiko.SSHClient, remotepath: str, localpath: str):
    """
        Pulls the contents of a file to a local path using a primitive 'cat' command.

        :param ssh_client: A paramiko.SSHClient to run commands over.
        :param remotepath: The path to the file on the remote machine.
        :param localpath: The local path to a file to write the contents of the remote file too.
    """
    copycmd = "cat %s" % remotepath

    status, stdout, stderr = ssh_execute_command(ssh_client, copycmd, decode=False)

    if status != 0:
        stderr = stderr.decode()
        errmsg_lines = [
            "Error pulling file using command. cmd=%s" % copycmd,
            "STDERR:",
            indent_lines(stderr, 1)
        ]
        raise Exception(os.linesep.join(errmsg_lines))

    with open(localpath, 'wb') as lfile:
        lfile.write(stdout)

    return

def primitive_file_push(ssh_client: paramiko.SSHClient, localpath: str, remotepath: str, read_size: int=1024):
    """
        Pushes the contents of a local file to a file on a remote machine at the path specified by remotepath.

        :param ssh_client: A paramiko.SSHClient to run commands over.
        :param localpath: The local path to a file to read contents from.
        :param remotepath: The path to file on the remote machine to write the contents of the local file too.
    """
    cat_cmd = "cat > {}".format(remotepath)

    with open(localpath, "rb") as file:
        content = file.read()
        status, stdout, stderr = ssh_execute_command(ssh_client, command=cat_cmd, chunk_size=read_size, input=content, decode=False)
        if status != 0:
            errmsg = "Error pushing file={} to remote path.".format(remotepath)
            fmt_errmsg = format_command_result(errmsg, status, stdout.decode(), stderr.decode())
            raise AKitCommandError(fmt_errmsg)

    return

def sftp_list_directory(sftp, directory, userlookup, grouplookup) -> dict:
    """
        Gets a listing of the directory entries of a remote directory.

        :param sftp: A paramiko.SFTPClient that is connected to a remote machine.
        :param directory: The remote directory to get the directory listing for.
        :param userlookup: A dictionary to utilize in order to lookup the user associated with a directory item.
        :param grouplookup: A dictionary to utilize in order to lookup the group associated with a directory item.

        :returns: A dictionary with the information about the items in the target directory.
    """
    entries = {}

    try:
        sftp.chdir(directory)
        directory_items = sftp.listdir()

        for nname in directory_items:

            try:
                ninfo = sftp.lstat(nname)
                perms = ""
                dentry = {
                    "name": nname,
                    "perms": perms,
                    "type": lookup_entry_type(directory, nname, ninfo),
                    "owner": userlookup(ninfo.st_uid),
                    "group": grouplookup(ninfo.st_gid),
                    "size": ninfo.st_size,
                    "accessed": ninfo.st_atime,
                    "modified": ninfo.st_mtime
                }

                entries[nname] = dentry
            except PermissionError:
                logger.exception("Unable to perform lstat on remote directory item %r." % nname)
    except PermissionError:
        logger.exception("Unable to perform listdir on remote directory %r." % directory)

    return entries

def sftp_list_tree(sftp: paramiko.SFTPClient, treeroot: str, userlookup: Callable[[int, Optional[bool]], str], grouplookup: Callable[[int, Optional[bool]], str], max_depth: int=1) -> dict:
    """
        Gets a tree of the directory entries of a remote directory.

        :param sftp: A paramiko.SFTPClient that is connected to a remote machine.
        :param treeroot: The root directory to get the directory listing for.
        :param userlookup: A dictionary to utilize in order to lookup the user associated with a directory item.
        :param grouplookup: A dictionary to utilize in order to lookup the group associated with a directory item.
        :param max_depth: The depth to which to create a directory tree.

        :returns: A dictionary with the information about the root directory and its children.
    """
    level_items = sftp_list_directory(sftp, treeroot, userlookup, grouplookup)

    if max_depth > 1:
        if not treeroot.endswith("/"):
            treeroot = treeroot + "/"

        for nxtitem in level_items.values():
            nxtname = nxtitem["name"]
            if nxtitem["type"] == "dir":
                nxtroot = treeroot + nxtname
                nxtchildren = sftp_list_tree_recurse(sftp, nxtroot, userlookup, grouplookup, max_depth - 1)
                nxtitem.update(nxtchildren)

    tree_info = {
        "name": treeroot,
        "items": level_items
    }

    return tree_info

def sftp_list_tree_recurse(sftp: paramiko.SFTPClient, targetdir: str, userlookup: Callable[[int, Optional[bool]], str], grouplookup: Callable[[int, Optional[bool]], str], remaining: int) -> dict:
    """
        Gets a listing of the directory passed and then recursively calls itself to create sub directory listings up to the remaining depth.

        :param sftp: A paramiko.SFTPClient that is connected to a remote machine.
        :param targetdir: The target directory to get the directory tree listing for.
        :param userlookup: A dictionary to utilize in order to lookup the user associated with a directory item.
        :param grouplookup: A dictionary to utilize in order to lookup the group associated with a directory item.
        :param max_depth: The depth to which to create a directory tree.

        :returns: A dictionary with the information about the target directory and its children.
    """
    level_items = sftp_list_directory(sftp, targetdir, userlookup, grouplookup)

    if remaining > 1:
        if not targetdir.endswith("/"):
            targetdir = targetdir + "/"

        for nxtitem in level_items.values():
            nxtname = nxtitem["name"]
            if nxtitem["type"] == "dir":
                nxtroot = targetdir + nxtname
                nxtchildren = sftp_list_tree_recurse(sftp, nxtroot, userlookup, grouplookup, remaining - 1)
                nxtitem.update(nxtchildren)

    children_info = {
        "items": level_items
    }

    return children_info

def ssh_execute_command(ssh_client: paramiko.SSHClient, command: str, pty_params=None,
                        inactivity_timeout: float=DEFAULT_SSH_TIMEOUT, inactivity_interval: float=DEFAULT_SSH_RETRY_INTERVAL,
                        chunk_size: int=1024, input: Optional[str]=None, decode=True) -> Tuple[int, str, str]:
    """
        Runs a command on a remote server using the specified ssh_client.  We implement our own version of ssh_execute_command
        in order to have better control over the timeouts and to make sure all the checks are sequenced properly in order
        to prevent SSH lockups.

        :param ssh_client: The :class:`paramiko.SSHClient` object to utilize when running the command.
        :param command: The commandline to run.
        :param inactivity_timeout: The timeout for the channel for the ssh transaction.
        :param inactivity_interval: The retry interval to wait for the channel to have data ready.
        :param chunk_size: The size of the chunks that are read during receive operations

        :returns: A tuple with the command result code, the standard output and the standard error output.
    """
    status = None
    stdout_buffer = bytearray()
    stderr_buffer = bytearray()

    start_time = time.time()
    end_time = start_time + inactivity_timeout

    channel = ssh_client.get_transport().open_session(timeout=inactivity_timeout)

    if pty_params is not None:
        channel.get_pty(**pty_params)

    channel.exec_command(command)

    input_length = 0
    if input is not None:
        if isinstance(input, str):
            input = input.encode()
        input_length = len(input)
    input_pos = 0
    input_shutdown = False

    while True:
        # Grab exit status ready before checking to see if stdout_ready or stderr_ready are True
        exit_status_ready = channel.exit_status_ready()
        stdout_ready = channel.recv_ready()
        stderr_ready = channel.recv_stderr_ready()

        # If stdout_ready or stderr_ready are true, we read this round
        if stdout_ready or stderr_ready:
            if stdout_ready:
                rcv_data = channel.recv(chunk_size)
                stdout_buffer.extend(rcv_data)
            if stderr_ready:
                rcv_data = channel.recv_stderr(chunk_size)
                stderr_buffer.extend(rcv_data)

            # We only want to timeout if there is inactivity
            start_time = time.time()
            end_time = start_time + inactivity_timeout

        # If there is data left to send and the send channel is ready
        # for input, send a chunk from the input buffer 
        elif input_length > 0 and input_pos < input_length and channel.send_ready():

            send_size = chunk_size
            avail_length = input_length - input_pos
            if avail_length < chunk_size:
                send_size = avail_length

            send_chunk = input[input_pos: input_pos + send_size]
            sent_size = channel.send(send_chunk)

            input_pos = input_pos + sent_size

        # If we have written everything there is to write, and writting to the
        # channel has not been shutdown, then shutdown writing.
        elif input is not None and not input_shutdown and input_pos >= input_length:
            channel.shutdown_write()
            input_shutdown = True

        # If we did not read any data this round and our exit status was ready, its time to exit
        elif exit_status_ready:
            status = channel.recv_exit_status()
            break
        # We didn't have any data to read and our exit status was not ready, go to sleep for interval
        else:
            now_time = time.time()
            if now_time > end_time:
                diff_time = now_time - start_time
                peername = ssh_client.get_transport().sock.getpeername()
                err_msg = "Timeout while executing SSH command.\n  peer=%r  command=%s\n  start=%r end=%r now=%r diff=%r" % (
                    peername, command, start_time, end_time, now_time, diff_time)
                raise TimeoutError(err_msg)

            # If we did not timeout, go to sleep for the interval before we make another attempt to read
            time.sleep(inactivity_interval)

        # End while True

    stdout = stdout_buffer
    if decode:
        stdout = stdout_buffer.decode()
    del stdout_buffer

    stderr = stderr_buffer
    if decode:
        stderr = stderr_buffer.decode()
    del stderr_buffer

    return status, stdout, stderr

def ssh_execute_command_in_channel(ssh_channel: paramiko.Channel, command: str, read_timeout: float=2, inactivity_timeout: float=DEFAULT_SSH_TIMEOUT, inactivity_interval: float=DEFAULT_SSH_RETRY_INTERVAL, chunk_size: int=1024, status_check=False) -> Tuple[int, str, str]:
    """
        Runs a command on a remote server using the specified ssh_client.  We implement our own version of ssh_execute_command
        in order to have better control over the timeouts and to make sure all the checks are sequenced properly in order
        to prevent SSH lockups.

        :param ssh_client: The :class:`paramiko.SSHClient` object to utilize when running the command.
        :param command: The commandline to run.
        :param inactivity_timeout: The timeout for the channel for the ssh transaction.
        :param inactivity_interval: The retry interval to wait for the channel to have data ready.
        :param chunk_size: The size of the chunks that are read during receive operations

        :returns: A tuple with the command result code, the standard output and the standard error output.
    """
    status = None
    stdout_buffer = bytearray()
    stderr_buffer = bytearray()

    start_time = time.time()
    end_time = start_time + inactivity_timeout

    ssh_channel.sendall(command + "\n")

    stdout_pipe_timeout = 0
    stderr_pipe_timeout = 0
    while True:
        if stdout_pipe_timeout < 2:
            try:
                rcv_data = ssh_channel.in_buffer.read(chunk_size, read_timeout)
                stdout_buffer.extend(rcv_data)
                if rcv_data.endswith(INTERACTIVE_PROMPT_BYTES):
                    stdout_pipe_timeout = 2
            except paramiko.buffered_pipe.PipeTimeout:
                stdout_pipe_timeout += 1

        if stderr_pipe_timeout < 2:
            try:
                rcv_data = ssh_channel.in_stderr_buffer.read(chunk_size, read_timeout)
                stderr_buffer.extend(rcv_data)
            except paramiko.buffered_pipe.PipeTimeout:
                stderr_pipe_timeout += 1

        if stdout_pipe_timeout > 1 and stderr_pipe_timeout > 1:
            break

        now_time = time.time()
        if now_time > end_time:
            errmsg = "Timeout while running command={}".format(command)
            raise AKitTimeoutError(errmsg)
        # End while True

    if not status_check:
        _, status_stdout, _ = ssh_execute_command_in_channel(ssh_channel, "echo $?", read_timeout=read_timeout, inactivity_timeout=inactivity_timeout, inactivity_interval=inactivity_interval, chunk_size=chunk_size, status_check=True)
        status = int(status_stdout)

    stdout = stdout_buffer.decode()
    del stdout_buffer

    if not stdout.startswith(command):
        errmsg = "The first line should have been an echo of our command."
        raise Exception(errmsg)

    if not stdout.endswith(INTERACTIVE_PROMPT):
        errmsg = "The first line should have been an echo of our command."
        raise Exception(errmsg)

    stdout = stdout[len(command):-len(INTERACTIVE_PROMPT)].strip()

    stderr = stderr_buffer.decode()
    del stderr_buffer

    return status, stdout, stderr


class SshBase(ICommandRunner):
    """
        The :class:`SshBase` object provides for the sharing of state and fuctional patterns
        for APIs between the :class:`SshSession` object and the :class:`SshAgent`.
    """
    def __init__(self, host: str, primary_credential: SshCredential, users: Optional[dict] = None,
                 port: int = 22, pty_params: Optional[dict] = None, called_id: Optional[str]=None,
                 aspects: AspectsCmd = DEFAULT_CMD_ASPECTS):

        self._host = host

        self._primary_credential = primary_credential
        self._username = primary_credential.username
        self._password = primary_credential.password
        self._keyfile = primary_credential.keyfile
        self._keypasswd = primary_credential.keypasswd
        self._allow_agent = primary_credential.allow_agent
        self._primitive = primary_credential.primitive

        self._users = users
        self._port = port
        self._pty_params = pty_params
        self._called_id = called_id
        self._target_tag = "[{}]".format(called_id)
        self._aspects = aspects

        self._ipaddr = socket.gethostbyname(self._host)

        self._user_lookup_table = {}
        self._group_lookup_table = {}

        if self._password is None and self._keyfile is None and not self._allow_agent:
            raise AKitInvalidConfigError("SshAgent requires either a 'password', an identity 'keyfile' or allow_agent=True be specified.") from None
        return

    @property
    def aspects(self) -> AspectsCmd:
        """
            The logging, iteration and other aspects that have been assigned to be used with interacting with the remote SSH service.
        """
        return self._aspects

    @property
    def host(self) -> str:
        """
            The target SSH host machine.
        """
        return self._host

    @property
    def ipaddr(self) -> str:
        """
            The IP address that was found to be associated with the specified host machine.
        """
        return self._ipaddr

    @property
    def port(self) -> int:
        """
            The port to use for SSH communications.  The default is 22.
        """
        return self._port

    @property
    def primary_credential(self):
        """
            Returns the 'primary' user credential provided for this ssh client object.
        """
        return self._primary_credential

    @property
    def pty_params(self) -> dict:
        """
            A dictionary of parameters that are to be passed when getting a PTY when interacting with the remote SSH server.
        """
        return self._pty_params

    @property
    def users(self) -> dict:
        """
            A dictionary of roles and user credentials that can be used for interaction with the remote SSH server.
        """
        return self._users

    def lookup_user_by_uid(self, uid: int, update: bool = True) -> Union[dict, None]:
        """
            A helper method used to lookup cached user information by uid.

            :param uid: The uid of a user.
            :param update: A boolean indicating that the table should be updated if the uid is not found.
        """
        username = None

        if uid in self._user_lookup_table:
            username = self._user_lookup_table[uid]
        elif update:
            status, stdout, _ = self.run_cmd("id -n -u %d" % uid)
            if status == 0:
                username = stdout.strip()
                self._user_lookup_table[uid] = username

        return username

    def lookup_group_by_uid(self, gid: int, update: bool = True) -> Union[dict, None]:
        """
            A helper method used to lookup cached group information by uid.

            :param gid: The gid of a group.
            :param update: A boolean indicating that the table should be updated if the uid is not found.

            :returns: The name of the group associated with the group id or None.
        """
        grpname = None

        if gid in self._group_lookup_table:
            grpname = self._group_lookup_table[gid]
        elif update:
            status, stdout, _ = self.run_cmd("id -n -g %d" % gid)
            if status == 0:
                grpname = stdout.strip()
                self._group_lookup_table[gid] = grpname

        return grpname

    def reboot(self, aspects: Optional[AspectsCmd] = None):
        """
            Reboots the designated host by running the 'reboot' command on the host.
            
            ..note: This method is not a typical SSH functionality, but it was added so that
                    automatic reconnects can be implemented as required on session objects.

        """
        raise AKitNotOverloadedError("SshBase.reboot must be overloaded by derived class '%s'." % type(self).__name__) from None
        reboot_cmd = 'reboot'
        try:
            status, stdout, stderr = self.run_cmd(reboot_cmd, aspects=aspects)
        except:
            # We might see a connection dropout exception here, so we need
            # to handle it.
            pass

        # Try to reconnect to the remote machine after the reboot.  We raise a AKitTimeoutError
        # if we do not reconnect before the reboot_timeout runs out.
        
        return

    def run_cmd(self, command: str, exp_status: Union[int, Sequence]=0, user: str = None, pty_params: dict = None, aspects: Optional[AspectsCmd] = None) -> Tuple[int, str, str]:
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
            :param exp_status: An integer or sequence of integers that specify the set of expected status codes from the command.
            :param user: The registered name of the user role to use to lookup the credentials for running the command.
            :param pty_params: The pty parameters to use to request a PTY when running the command.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """
        raise AKitNotOverloadedError("SshBase.run_cmd must be overloaded by derived class '%s'." % type(self).__name__) from None

    def verify_connectivity(self) -> bool:
        """
            Method that can be used to verify connectivity to the target computer.

            :returns: A boolean value indicating whether connectivity with the remote machine was successful.
        """
        vok = False

        hello_cmd = "echo Hello"
        status, stdout, _ = self.run_cmd(hello_cmd)
        if status == 0 and stdout.strip() == "Hello":
            vok = True

        return vok

    def _create_client(self, session_user: Optional[str] = None) -> paramiko.SSHClient:
        """
            Create an SSHClient to use for running commands and performing FTP operations.

            :param session_user: The user role and associated credentials to use when creating the SSHClient.

            :returns: An SSHClient object connected to the remote machine under the default or specified user credential.
        """
        cl_username = self._username
        cl_password = self._password
        cl_keyfile = self._keyfile
        cl_keypasswd = self._keypasswd
        cl_allow_agent = self._allow_agent

        if session_user is not None:
            if session_user not in self._users:
                errmsg_list = [
                    "No credentials found for the specified user '%s'." % session_user
                ]
                errmsg = os.linesep.join(errmsg_list)
                raise AKitInvalidConfigError(errmsg) from None

            user_creds = self._users[session_user]

            cl_username = user_creds["username"]
            cl_password = user_creds["password"]
            cl_keyfile = user_creds["keyfile"]
            cl_keypasswd = user_creds["keypasswd"]
            cl_allow_agent = user_creds["allow_agent"]

        pkey = None
        if cl_keyfile is not None:
            cl_keyfile = os.path.expanduser(os.path.expandvars(cl_keyfile))
            pkey = paramiko.rsakey.RSAKey.from_private_key_file(cl_keyfile, password=cl_keypasswd)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self._ipaddr, port=self._port, username=cl_username, password=cl_password, pkey=pkey, allow_agent=cl_allow_agent)
        return ssh_client

    def _directory(self, ssh_client: paramiko.SSHClient, root_dir: str) -> dict:
        """
            Private method that creates a directory listing for the folder.

            :param ssh_client: The SSHClient to use to for geting a list tree.
            :param root_dir: The directory to scan when creating the tree.

            :returns: A dictionary that contains information about the items in the target directory.
        """
        dir_info = {}

        if not self._primitive:
            transport = ssh_client.get_transport()
            try:

                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    dir_info = sftp_list_directory(sftp, root_dir, self.lookup_user_by_uid, self.lookup_group_by_uid)
                finally:
                    sftp.close()
            finally:
                transport.close()
        else:
            dir_info = primitive_list_directory(ssh_client, root_dir)

        return dir_info

    def _directory_exists(self, ssh_client: paramiko.SSHClient, remotedir: str) -> bool:
        """
            Private helper method used to check if the remote directory exists.
        """
        exists = False

        if not self._primitive:
            transport = ssh_client.get_transport()
            try:
                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    fsresult = sftp.stat(remotedir)
                    if fsresult.st_mode | stat.S_IFDIR:
                        exists = True
                finally:
                    sftp.close()
            finally:
                transport.close()
        else:
            primitive_directory_exists(ssh_client, remotedir)

        return exists

    def _directory_tree(self, ssh_client: paramiko.SSHClient, root_dir: str, depth: int = 1) -> dict:
        """
            Private method that creates a directory tree for the folder.

            :param ssh_client: The SSHClient to use to for geting a list tree.
            :param root_dir: The root directory to scan when creating the tree.
            :param depth: The dept to scan to

            :returns: A dictionary with a tree of information about the directory tree found on the remote system.
        """
        dir_info = {}

        if not self._primitive:
            transport = ssh_client.get_transport()
            try:

                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    dir_info = sftp_list_tree(sftp, root_dir, self.lookup_user_by_uid, self.lookup_group_by_uid, max_depth=depth)
                finally:
                    sftp.close()
            finally:
                transport.close()
        else:
            dir_info = primitive_list_tree(ssh_client, root_dir, max_depth=depth)

        return dir_info

    def _log_command_result(self, command: str, status: int, stdout: str, stderr: str, exp_status: Union[int, Sequence[int]], logging_pattern: LoggingPattern):
        """
            Private method that handles the logging of command results based on the expected status and logging pattern
            specified.

            :param command: The command that was run.
            :param status: The status code returned from running the command.
            :param stdout: The contents of the standard output from running the command.
            :param stderr: The contents of the error output from running the command.
            :param exp_status: The status code or possible status codes that was expected to be returned from running the command.
            :param logging_pattern: The result logging pattern (LoggingPattern) to use when logging.
        """
        # pylint: disable=no-self-use

        tgt_tag = ""
        if self._target_tag is not None:
            tgt_tag = self._target_tag

        if isinstance(exp_status, int):
            if status == exp_status:
                if logging_pattern == LoggingPattern.ALL_RESULTS or logging_pattern == LoggingPattern.SUCCESS_ONLY:
                    logger.info(TEMPLATE_COMMAND_SUCCESS % (tgt_tag, command, stdout, stderr) )
        else:
            if status in exp_status:
                if logging_pattern == LoggingPattern.ALL_RESULTS or logging_pattern == LoggingPattern.SUCCESS_ONLY:
                    logger.info(TEMPLATE_COMMAND_SUCCESS % (tgt_tag, command, stdout, stderr))
            else:
                if logging_pattern == LoggingPattern.ALL_RESULTS or logging_pattern == LoggingPattern.FAILURE_ONLY:
                    logger.error(TEMPLATE_COMMAND_FAILURE % (tgt_tag, command, stdout, stderr))

        return

    def _run_cmd(self, ssh_runner: Union[paramiko.SSHClient, paramiko.Channel], command: str, exp_status: Union[int, Sequence]=0, user: str = None, pty_params: dict = None, aspects: Optional[AspectsCmd] = None) -> Tuple[int, str, str]:
        """
            Private method that handles the running commands in a generic way so the logic and run pattern code can be shared between agent and session objects.

            :param ssh_runner: A :class:`paramiko.SSHClient` or :class:`paramiko.Channel` object that can be used to run a command on a remote machine.
            :param command: The command that is to be run.
            :param exp_status: The status code or a sequence of possible status codes that are expected to be returned from running the command.
            :param user: The role name of the user account to utilize when looking up the credentials used to connect to the remote host.
            :param pty_params: A dictionary of parameters that are passed to paramiko to get a pty when running commands.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """
        # Go through the overrides and if they are not passed use the agent defaults.
        if pty_params is None:
            pty_params = self._pty_params

        if aspects is None:
            aspects = self._aspects

        if user is not None:
            if self._users is None:
                errmsg = "In order to pass a 'user' parameter, you must create the SSHAgent with a 'users' parameter with a dictionary of user credentials."
                raise AKitInvalidConfigError(errmsg) from None
            if user not in self._users:
                errmsg = "The specified 'user=%s' was not found in the users credentials provided to SSHAgent."

        completion_toctx = TimeoutContext(aspects.completion_timeout, aspects.completion_interval)
        
        inactivity_timeout = aspects.inactivity_timeout
        inactivity_interval = aspects.inactivity_interval
        monitor_delay = aspects.monitor_delay
        logging_pattern = aspects.logging_pattern

        status, stdout, stderr = None, None, None

        this_thr = threading.current_thread()
        monmsg= "Thread failed to exit monitored scope. thid=%s thname=%s cmd=%s" % (this_thr.ident, this_thr.name, command)

        # Run the command using the SINGULAR pattern, we run it once and then return the result
        if aspects.action_pattern == ActionPattern.SINGLE_CALL:

            # Setup a monitored scope for the call to the remote device in case of timeout failure
            with MonitoredScope("RUNCMD-SINGULAR", monmsg, completion_toctx, notify_delay=monitor_delay) as _:

                status, stdout, stderr = self._ssh_execute_command(ssh_runner, command, pty_params=pty_params,
                    inactivity_timeout=inactivity_timeout, inactivity_interval=inactivity_interval)

            self._log_command_result(command, status, stdout, stderr, exp_status, logging_pattern)

        # DO_UNTIL_SUCCESS, run the command until we get a successful expected result or a completion timeout has occured
        elif aspects.action_pattern == ActionPattern.DO_UNTIL_SUCCESS:

            completion_toctx.mark_begin()

            while True:

                # Setup a monitored scope for the call to the remote device in case of timeout failure
                with MonitoredScope("RUNCMD-DO_UNTIL_SUCCESS", monmsg, completion_toctx, notify_delay=monitor_delay) as _:
                    status, stdout, stderr = self._ssh_execute_command(ssh_runner, command, pty_params=pty_params,
                        inactivity_timeout=inactivity_timeout, inactivity_interval=inactivity_interval)

                self._log_command_result(command, status, stdout, stderr, exp_status, logging_pattern)

                if isinstance(exp_status, int):
                    if status == exp_status:
                        break
                elif status in exp_status:
                    break

                if completion_toctx.final_attempt:
                    what_for="command success"
                    details = [
                        "CMD: %s" % command,
                        "STDOUT:",
                        indent_lines(stdout, 1),
                        "STDERR:",
                        indent_lines(stderr, 1),
                    ]
                    toerr = completion_toctx.create_timeout(what_for=what_for, detail=details)
                    raise toerr

                elif not completion_toctx.should_continue():
                    completion_toctx.mark_final_attempt()

                time.sleep(completion_toctx.interval)

        # DO_WHILE_SUCCESS, run the command while it is succeeds or a completion timeout has occured
        elif aspects.action_pattern == ActionPattern.DO_WHILE_SUCCESS:

            completion_toctx.mark_begin()

            while True:

                with MonitoredScope("RUNCMD-DO_WHILE_SUCCESS", monmsg, completion_toctx, notify_delay=monitor_delay) as _:
                    status, stdout, stderr = self._ssh_execute_command(ssh_runner, command, pty_params=pty_params,
                        inactivity_timeout=inactivity_timeout, inactivity_interval=inactivity_interval)

                self._log_command_result(command, status, stdout, stderr, exp_status, logging_pattern)

                if isinstance(exp_status, int):
                    if status != exp_status:
                        break
                elif status not in exp_status:
                    break

                if completion_toctx.final_attempt:
                    what_for="command failure"
                    details = [
                        "CMD: %s" % command,
                        "STDOUT:",
                        indent_lines(stdout, 1),
                        "STDERR:",
                        indent_lines(stderr, 1),
                    ]
                    toerr = completion_toctx.create_timeout(what_for=what_for, detail=details)
                    raise toerr

                elif not completion_toctx.should_continue():
                    completion_toctx.mark_final_attempt()

                time.sleep(completion_toctx.interval)

        elif aspects.action_pattern == ActionPattern.SINGLE_CONNECTED_CALL or aspects.action_pattern == ActionPattern.DO_UNTIL_CONNECTION_FAILURE:
            errmsg = "SshAgent and SshSession currently do not support the SINGLE_CONNECTED_CALL or DO_UNTIL_CONNECTION_FAILURE action patterns."
            raise AKitSemanticError(errmsg) from None
        else:
            errmsg = "SshBase: Unknown ActionPattern encountered. action_pattern={}".format(aspects.action_pattern)
            raise AKitSemanticError(errmsg) from None

        return status, stdout, stderr

    def _file_exists(self, ssh_client: paramiko.SSHClient, remotepath: str) -> bool:
        """
            Private helper method used to check if the remote file exists.
        """
        exists = False

        if not self._primitive:
            transport = ssh_client.get_transport()
            try:
                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    fsresult = sftp.stat(remotepath)
                    if not (fsresult.st_mode | stat.S_IFDIR):
                        exists = True
                finally:
                    sftp.close()
            finally:
                transport.close()
        else:
            primitive_file_exists(ssh_client, remotepath)

        return exists

    def _file_pull(self, ssh_client: paramiko.SSHClient, remotepath: str, localpath: str):
        """
            Private helper method used to pull a remote file to a local file path.
        """
        if not self._primitive:
            transport = ssh_client.get_transport()
            try:
                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    sftp.get(remotepath, localpath)
                finally:
                    sftp.close()
            finally:
                transport.close()
        else:
            primitive_file_pull(ssh_client, remotepath, localpath)

        return

    def _file_push(self, ssh_client: paramiko.SSHClient, localpath: str, remotepath: str):
        """
            Private helper method used to push a local file to a remote file path.
        """
        if not self._primitive:
            transport = ssh_client.get_transport()
            try:
                sftp = paramiko.SFTPClient.from_transport(transport)
                try:
                    sftp.put(localpath, remotepath)
                finally:
                    sftp.close()
            finally:
                transport.close()
        else:
            primitive_file_push(ssh_client, localpath, remotepath)

        return

    def _ssh_execute_command(self, ssh_runner, command: str, pty_params=None, inactivity_timeout: float=DEFAULT_SSH_TIMEOUT, inactivity_interval: float=DEFAULT_SSH_RETRY_INTERVAL, chunk_size: int=1024) -> Tuple[int, str, str]: # pylint: disable=no-self-use
        """
            Private helper method used to route the command running parameters to the correct routine based on whether the command is being run interactively
            through a session or is a single run command from an SshAgent.

            :param ssh_runner: A :class:`paramiko.SSHClient` or :class:`paramiko.Channel` object that can be used to run a command on a remote machine.
            :param command: The command that is to be run.
            :param pty_params: A dictionary of parameters that are passed to paramiko to get a pty when running commands.
            :param inactivity_timeout: A timeout for inactivity between the local machine and remote machine.
            :param inactivity_interval: The interval to wait between attempts to interact or read from the remote machine.
            :param chunk_size: The size of the buffer to use when reading results from the remote machine.
        """
        status, stdout, stderr = ssh_execute_command(ssh_runner, command, pty_params=pty_params, inactivity_timeout=inactivity_timeout, inactivity_interval=inactivity_interval, chunk_size=chunk_size)
        return status, stdout, stderr


class SshSession(SshBase):
    """
        The :class:`SshSession` provides an extension of the :class:`SshBase` class interface and api(s).  The :class:`SshSession` serves to
        act as a session scoping object that establishes a set of SSH credentials, settings and patterns that are to be used for a series of
        SSH operations.  The :class:`SshSession` also holds open the SSHClient for its entire scope and ensures the SSHClient is closed and
        cleaned up properly when the :class:`SshSession` goes out of scope.
    """
    def __init__(self, host: str, primary_credential: SshCredential, users: Optional[dict] = None, port:int=22,
                 pty_params: Optional[dict] = None, session_user=None, interactive=False, basis_session: Optional["SshSession"]=None,
                 called_id: Optional[str]=None, aspects: AspectsCmd=DEFAULT_CMD_ASPECTS):
        SshBase.__init__(self, host, primary_credential, users=users, port=port, pty_params=pty_params, called_id=called_id, aspects=aspects)

        self._session_user = session_user
        self._interactive = interactive
        self._read_timeout = 2

        self._ssh_client = None
        self._ssh_runner = None
        self._basis_session = basis_session
        return

    def __enter__(self):
        """
            Method that implements the __enter__ symantics used for 'with' statements.
        """
        self._ssh_client = self._create_client()

        if self._interactive:
            inactivity_timeout = self._aspects.inactivity_timeout

            channel = self._ssh_client.get_transport().open_session(timeout=inactivity_timeout)

            if self._pty_params is not None:
                channel.get_pty(**self._pty_params)
            else:
                channel.get_pty()

            channel.invoke_shell()
            channel.sendall("export PS1=%s\n" % INTERACTIVE_PROMPT)

            leader = b""
            try:
                while True:
                    out = channel.in_buffer.read(1028, self._read_timeout)
                    leader += out
            except paramiko.buffered_pipe.PipeTimeout as _:
                # We don't need to do anything if the pipe, times out.
                # it means we are likely at the command prompt and that
                # there is nothing to read.
                pass

            self._ssh_runner = channel
        else:
            self._ssh_runner = self._ssh_client

        return self

    def __exit__(self, ex_type: type, ex_val: Exception, ex_tb: TracebackType) -> bool:
        """
            Method that implements the __exit__ symantics used for 'with' statements.

            :returns: Returns false indicating that exceptions are not handled.
        """
        self.close()
        handled = False
        return handled

    def close(self):
        """
            Closes the SSH session and the assocatied SSH connection.
        """
        # Only close the client if this session owns the client
        if self._basis_session is None:
            self._ssh_client.close()
        return

    def reboot(self, aspects: Optional[AspectsCmd] = None):
        """
            Reboots the designated host by running the 'reboot' command on the host.
            
            ..note: This method is not a typical SSH functionality, but it was added so that
                    automatic reconnects can be implemented as required on session objects.

        """
        reboot_cmd = 'reboot'
        try:
            status, stdout, stderr = self.run_cmd(reboot_cmd, aspects=aspects)
        except:
            # We might see a connection dropout exception here, so we need
            # to handle it.
            pass

        # Since we are a session, we need to reconnect to the remote machine after the reboot.
        # We raise a AKitTimeoutError if we do not reconnect before the reboot_timeout runs out.
        
        return

    def run_cmd(self, command: str, exp_status: Union[int, Sequence]=0, user: str = None, pty_params: dict = None, aspects: Optional[AspectsCmd] = None) -> Tuple[int, str, str]:
        """
            Runs a command on the designated host using the current session SSH session and client.

            :param command: The command to run.
            :param exp_status: An integer or sequence of integers that specify the set of expected status codes from the command.
            :param user: The registered name of the user role to use to lookup the credentials for running the command.
            :param pty_params: The pty parameters to use to request a PTY when running the command.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """

        status, stdout, stderr = self._run_cmd(self._ssh_runner, command, user=user, pty_params=pty_params, aspects=aspects)

        return status, stdout, stderr

    def directory(self, root_dir: str) -> dict:
        """
            Method that creates a directory listing for the folder.

            :param root_dir: The directory to scan when creating the tree.

            :returns: A dictionary that contains information about the items in the target directory.
        """
        dir_info = self._directory(self._ssh_client, root_dir)

        return dir_info

    def directory_exists(self, remotedir: str) -> bool:
        """
            Method used to pull a remote directory to check for existance.

            :param remotedir: The remote directory path to check for existance.

            :returns: A boolean value indicating if the remote file exists.
        """
        exists = self._file_pull(self._ssh_client, remotedir)

        return exists

    def directory_tree(self, root_dir: str, depth: int = 1) -> dict:
        """
            Method that creates a directory tree for the folder.

            :param root_dir: The root directory to scan when creating the tree.
            :param depth: The dept to scan to

            :returns: A dictionary with a tree of information about the directory tree found on the remote system.
        """
        dir_info = self._directory_tree(self._ssh_client, root_dir, depth=depth)

        return dir_info

    def file_exists(self, remotepath: str) -> bool:
        """
            Method used to pull a remote file to check for existance.

            :param remotepath: The remote file path to check for existance.

            :returns: A boolean value indicating if the remote file exists.
        """
        exists = self._file_pull(self._ssh_client, remotepath)

        return exists

    def file_pull(self, remotepath: str, localpath: str):
        """
            Method used to pull a remote file to a local file path.

            :param remotepath: The remote file path to pull to the local file.
            :param localpath: The local file path to pull the content to.
        """
        self._file_pull(self._ssh_client, remotepath, localpath)

        return

    def file_push(self, localpath: str, remotepath: str):
        """
            Method used to push a local file to a remote file path.

            :param localpath: The local file path to push the content of to the remote file.
            :param remotepath: The remote file path to push content to.
        """
        self._file_push(self._ssh_client, localpath, remotepath)

        return

    def open_session(self, primitive: bool = False, pty_params: Optional[dict] = None, interactive=False, basis_session: Optional["SshSession"] = None,
                     aspects: Optional[AspectsCmd] = None) -> "SshSession":
        """
            Provies a mechanism to create a :class:`SshSession` object with derived settings.  This method allows various parameters for the session
            to be overridden.  This allows for the performing of a series of SSH operations under a particular set of shared settings and or credentials.

            :param primitive: Use primitive mode for FTP operations for the session.
            :param pty_params: The default pty parameters to use to request a PTY when running commands through the session.
            :param interactive: Creates an interactive session which holds open an interactive shell so commands can interact in the shell.
            :param basis_session: An optional SshSession instance to use as a session basis.  This allows re-use of sessions.
            :param aspects: The default run aspects to use for the operations performed by the session.
        """

        if aspects is None:
            aspects = self._aspects

        session = None
        if basis_session is not None:
            bs = basis_session
            session = SshSession(bs._host, bs._primary_credential, users=bs._users, port=bs._port, pty_params=pty_params,
                             interactive=interactive, basis_session=basis_session, aspects=aspects)
        else:
            session = SshSession(self._host, self._primary_credential, users=self._users, port=self._port, pty_params=pty_params,
                             interactive=interactive, basis_session=basis_session, aspects=aspects)
        return session

    def _create_client(self, session_user: Optional[str] = None) -> paramiko.SSHClient:
        """
            Create an SSHClient to use for running commands and performing FTP operations.

            :param session_user: The user role and associated credentials to use when creating the SSHClient.

            :returns: An SSHClient object connected to the remote machine under the default or specified user credential.
        """
        ssh_client = None
        if self._basis_session is not None:
            ssh_client = self._basis_session._ssh_client
        else:
            ssh_client = SshBase._create_client(self, session_user=session_user)
        return ssh_client

    def _ssh_execute_command(self, ssh_runner, command: str, pty_params=None, inactivity_timeout: float=DEFAULT_SSH_TIMEOUT, inactivity_interval: float=DEFAULT_SSH_RETRY_INTERVAL, chunk_size: int=1024) -> Tuple[int, str, str]:
        """
            Private helper method used to route the command running parameters to the correct routine based on whether the command is being run interactively
            through a session or is a single run command from an SshAgent.

            :param ssh_runner: A :class:`paramiko.SSHClient` or :class:`paramiko.Channel` object that can be used to run a command on a remote machine.
            :param command: The command that is to be run.
            :param pty_params: A dictionary of parameters that are passed to paramiko to get a pty when running commands.
            :param inactivity_timeout: A timeout for inactivity between the local machine and remote machine.
            :param inactivity_interval: The interval to wait between attempts to interact or read from the remote machine.
            :param chunk_size: The size of the buffer to use when reading results from the remote machine.
        """
        if self._interactive:
            status, stdout, stderr = ssh_execute_command_in_channel(ssh_runner, command, read_timeout=self._read_timeout, inactivity_timeout=inactivity_timeout, inactivity_interval=inactivity_interval)
        else:
            status, stdout, stderr = ssh_execute_command(ssh_runner, command, pty_params=pty_params, inactivity_timeout=inactivity_timeout, inactivity_interval=inactivity_interval)
        return status, stdout, stderr

class SshAgent(SshBase, LandscapeDeviceExtension):
    """
        The :class:`SshAgent` provides an extension of the :class:`SshBase` class interface and api(s).  The :class:`SshAgent` manages connection
        and interop settings that are used to perform operations and interact with a remote SSH service.  The :class:`SshAgent` provides standard
        APIs for running command and transferring files along with code that helps ensure commands are logged cleanly.  The :class:`SshAgent` also
        provides run patterning to help eliminate duplication of code associated with running SSH commands in loops.
    """
    def __init__(self, host: str, primary_credential: SshCredential, users: Optional[dict] = None, port: int = 22,
                 pty_params: Optional[dict] = None, called_id: Optional[str]=None, aspects: AspectsCmd = DEFAULT_CMD_ASPECTS):
        SshBase.__init__(self, host, primary_credential, users=users, port=port, pty_params=pty_params, called_id=called_id, aspects=aspects)
        LandscapeDeviceExtension.__init__(self)
        return

    def initialize(self, coord_ref: weakref.ReferenceType, basedevice_ref: weakref.ReferenceType, extid: str, location: str, configinfo: dict):
        """
            Initializes the landscape device extension. It is not required to call this function in order to use an SSHAgent, it is used
            when an agent is attached to a LandscapeDevice as a device extension.

            :param coord_ref: A weak reference to the coordinator that is managing interactions through this
                              device extension.
            :param extid: A unique reference that can be used to identify this device via the coordinator even if its location changes.
            :param location: The location reference where this device can be found via the coordinator.
            :param configinfo: The configuration information dictionary from the landscape file for the specified host.
        """
        LandscapeDeviceExtension.initialize(self, coord_ref, basedevice_ref, extid, location, configinfo)
        return

    def open_session(self, primitive: bool = False, pty_params: Optional[dict] = None, interactive=False, basis_session: Optional[SshSession] = None,
                     aspects: Optional[AspectsCmd] = None) -> SshSession:
        """
            Provies a mechanism to create a :class:`SshSession` object with derived settings.  This method allows various parameters for the session
            to be overridden.  This allows for the performing of a series of SSH operations under a particular set of shared settings and or credentials.

            :param primitive: Use primitive mode for FTP operations for the session.
            :param pty_params: The default pty parameters to use to request a PTY when running commands through the session.
            :param interactive: Creates an interactive session which holds open an interactive shell so commands can interact in the shell.
            :param basis_session: An optional SshSession instance to use as a session basis.  This allows re-use of sessions.
            :param aspects: The default run aspects to use for the operations performed by the session.
        """

        if aspects is None:
            aspects = self._aspects

        session = None
        if basis_session is not None:
            bs = basis_session
            session = SshSession(bs._host, bs._primary_credential, users=bs._users, port=bs._port, pty_params=pty_params,
                             interactive=interactive, basis_session=basis_session, aspects=aspects)
        else:
            session = SshSession(self._host, self._primary_credential, users=self._users, port=self._port, pty_params=pty_params,
                             interactive=interactive, basis_session=basis_session, aspects=aspects)
        return session

    def reboot(self, aspects: Optional[AspectsCmd] = None):
        """
            Reboots the designated host by running the 'reboot' command on the host.
            
            ..note: This method is not a typical SSH functionality, but it was added so that
                    automatic reconnects can be implemented as required on session objects.

        """
        reboot_cmd = 'reboot'
        try:
            status, stdout, stderr = self.run_cmd(reboot_cmd, aspects=aspects)
        except:
            # We might see a connection dropout exception here, so we need
            # to handle it.
            pass

        # Since we are NOT a session, we need to verify the remote machine is back up by attempting to
        # connect to the machine and run a command. We raise a AKitTimeoutError if we cannot connect and
        # run a command before the reboot_timeout runs out.
        
        return

    def run_cmd(self, command: str, exp_status: Union[int, Sequence]=0, user: str = None, pty_params: dict = None, aspects: Optional[AspectsCmd] = None, ssh_client: Optional[paramiko.SSHClient]=None) -> Tuple[int, str, str]: # pylint: disable=arguments-differ
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
            :param exp_status: An integer or sequence of integers that specify the set of expected status codes from the command.
            :param user: The registered name of the user role to use to lookup the credentials for running the command.
            :param pty_params: The pty parameters to use to request a PTY when running the command.
            :param aspects: The run aspects to use when running the command.
            :param ssh_client: An optional connected SSHClient that should be for the operation.

            :returns: The status, stderr and stdout from the command that was run.
        """
        cleanup_client = False

        status, stdout, stderr = None, None, None

        try:
            if ssh_client is None:
                # If we are not passed in a client to use, we create one
                # and then clean it up before returning
                ssh_client = self._create_client()
                cleanup_client = True

            status, stdout, stderr = self._run_cmd(ssh_client, command, exp_status=exp_status, user=user, pty_params=pty_params, aspects=aspects)

        finally:
            # If we created a client, clean it up
            if cleanup_client:
                ssh_client.close()
                del ssh_client

        return status, stdout, stderr

    def directory_tree(self, root_dir: str, depth: int = 1, ssh_client: Optional[paramiko.SSHClient] = None) -> dict:
        """
            Method that creates a directory tree for the folder.

            :param root_dir: The root directory to scan when creating the tree.
            :param depth: The dept to scan to
            :param ssh_client: An optional connected SSHClient that should be for the operation.

            :returns: A dictionary with a tree of information about the directory tree found on the remote system.
        """
        dir_info = {}

        cleanup_client = False
        try:
            if ssh_client is None:
                ssh_client = self._create_client()
                cleanup_client = True

            dir_info = self._directory_tree(ssh_client, root_dir, depth=depth)

        finally:
            if cleanup_client:
                ssh_client.close()
                del ssh_client

        return dir_info

    def directory(self, root_dir: str, ssh_client: Optional[paramiko.SSHClient] = None) -> dict:
        """
            Method that creates a directory listing for the folder.

            :param root_dir: The directory to scan when creating the tree.
            :param ssh_client: An optional connected SSHClient that should be for the operation.

            :returns: A dictionary that contains information about the items in the target directory.
        """
        dir_info = {}

        cleanup_client = False
        try:
            if ssh_client is None:
                ssh_client = self._create_client()
                cleanup_client = True

            dir_info = self._directory(ssh_client, root_dir)

        finally:
            if cleanup_client:
                ssh_client.close()
                del ssh_client

        return dir_info

    def directory_exists(self, remotedir: str, ssh_client: Optional[paramiko.SSHClient] = None) -> bool:
        """
            Method used to check if a remote directory exists.

            :param remotedir: The remote remotedir path to check for existance.
            :param ssh_client: An optional connected SSHClient that should be for the operation.
        """
        exists = False

        try:
            if ssh_client is None:
                ssh_client = self._create_client()
                cleanup_client = True

            self._directory_exists(ssh_client, remotedir)

        finally:
            if cleanup_client:
                ssh_client.close()
                del ssh_client

        return exists

    def file_exists(self, remotepath: str, ssh_client: Optional[paramiko.SSHClient] = None) -> bool:
        """
            Method used to check if a remote file exists.

            :param remotepath: The remote file path to check for existance.
            :param ssh_client: An optional connected SSHClient that should be for the operation.
        """
        exists = False

        try:
            if ssh_client is None:
                ssh_client = self._create_client()
                cleanup_client = True

            self._file_exists(ssh_client, remotepath)

        finally:
            if cleanup_client:
                ssh_client.close()
                del ssh_client

        return exists

    def file_pull(self, remotepath: str, localpath: str, ssh_client: Optional[paramiko.SSHClient] = None):
        """
            Method used to pull a remote file to a local file path.

            :param remotepath: The remote file path to pull to the local file.
            :param localpath: The local file path to pull the content to.
            :param ssh_client: An optional connected SSHClient that should be for the operation.
        """
        cleanup_client = False
        try:
            if ssh_client is None:
                ssh_client = self._create_client()
                cleanup_client = True

            self._file_pull(ssh_client, remotepath, localpath)

        finally:
            if cleanup_client:
                ssh_client.close()
                del ssh_client

        return

    def file_push(self, localpath: str, remotepath: str, ssh_client: Optional[paramiko.SSHClient] = None):
        """
            Method used to push a local file to a remote file path.

            :param localpath: The local file path to push the content of to the remote file.
            :param remotepath: The remote file path to push content to.
            :param ssh_client: An optional connected SSHClient that should be for the operation.
        """
        cleanup_client = False
        try:
            if ssh_client is None:
                ssh_client = self._create_client()
                cleanup_client = True

            self._file_push(ssh_client, localpath, remotepath)

        finally:
            if cleanup_client:
                ssh_client.close()
                del ssh_client

        return
