
from typing import Tuple

import os
import threading

import multiprocessing
import multiprocessing.managers

from impacket import smbserver

DEFAULT_SMB_CHALLENGE = '4141414141414141'

class SimpleSMBServerProcess:
    def __init__(self, listenAddress='0.0.0.0', listenPort=445, configFile=''):
        self._smbsrvr = smbserver.SimpleSMBServer(listenAddress=listenAddress, listenPort=listenPort, configFile=configFile)
        self._thread = None
        return

    def addCredential(self, name, uid, lmhash, nthash):
        self._smbsrvr.addCredential(name, uid, lmhash, nthash)
        return

    def addShare(self, shareName, sharePath, shareComment='', shareType='0', readOnly='no'):
        self._smbsrvr.addShare(shareName, sharePath, shareComment=shareComment, shareType=shareType, readOnly=readOnly)
        return

    def getServerAddress(self):
        address = self._smbsrvr._SimpleSMBServer__server.server_address
        return address

    def getRegisteredNamedPipes(self):
        return self._smbsrvr.getRegisteredNamedPipes()

    def registerNamedPipe(self, pipeName, address):
        return self._smbsrvr.registerNamedPipe(pipeName, address)

    def removeShare(self, shareName):
        self._smbsrvr.removeShare(shareName)
        return

    def setCredentialsFile(self, credFile):
        self._smbsrvr.setCredentialsFile(credFile)
        return

    def setLogFile(self, logFile):
        self._smbsrvr.setLogFile(logFile)
        return

    def setSMB2Support(self, value):
        self._smbsrvr.setSMB2Support(value)
        return

    def setSMBChallenge(self, challenge):
        self._smbsrvr.setSMBChallenge(challenge)
        return

    def start(self):
        self._thread = threading.Thread(target=self._smbsrvr.start, name='smb-server-entry')
        self._thread.daemon = True
        self._thread.start()
        return

    def stop(self):
        self._smbsrvr.stop()
        return

    def unregisterNamedPipe(self, pipeName):
        return self._smbsrvr.unregisterNamedPipe(pipeName)


class SimpleSMBServerManager(multiprocessing.managers.BaseManager):
    """
        This is a process manager used for creating a :class:`SimpleWebServer`
        in a remote process that can be communicated with via a proxy.
    """

SimpleSMBServerManager.register("SimpleSMBServerProcess", SimpleSMBServerProcess)

def spawn_smbserver_process(rootshare: str, rootdir: str, rootdesc='Root SMB Share', endpoint: Tuple[str, int]=('0.0.0.0', 445),
                            challenge: str=DEFAULT_SMB_CHALLENGE, logfile: str='') -> Tuple[SimpleSMBServerManager, smbserver.SimpleSMBServer]:
    listenAddress, listenPort = endpoint

    rootdir = os.path.abspath(os.path.expanduser(os.path.expandvars(rootdir)))
    if len(logfile) > 0:
        logfile = os.path.abspath(os.path.expanduser(os.path.expandvars(logfile)))

    srvr_mgr = SimpleSMBServerManager()
    srvr_mgr.start()

    svr_proxy = srvr_mgr.SimpleSMBServerProcess(listenAddress=listenAddress, listenPort=listenPort)
    svr_proxy.setSMB2Support(True)
    svr_proxy.addShare(rootshare.upper(), rootdir)
    #svr_proxy.setSMBChallenge(challenge)
    svr_proxy.setLogFile(logfile)
    svr_proxy.start()

    return srvr_mgr, svr_proxy
