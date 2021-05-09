"""
.. module:: configuration
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the default runtime configration dictionary and the functions that
               are used to load the automation configuration file and overlay the settings on top of the
               default runtime configuration.

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

import collections
import os
import threading

RUNTIME_DEFAULTS = {
    "version": "1.0.0",
    "logging": {
        "levels": {
            "console": "INFO",
            "logfile": "DEBUG"
        },
        "logname": "%(jobtype)s.log",
        "branched": [
            {
                "name": "paramiko.transport",
                "logname": "paramiko.transport.log",
                "loglevel": "DEBUG"
            }
        ]
    },
    "paths": {
        "landscape": os.sep.join(("~", "akit", "config", "landscape.yaml")),
        "results": os.sep.join(("~", "akit", "results")),
        "consoleresults": os.sep.join(("~", "akit", "console", "%(starttime)s")),
        "runresults": os.sep.join(("~", "akit", "results", "runresults", "%(starttime)s")),
        "testresults": os.sep.join(("~", "akit", "results", "testresults", "%(starttime)s"))
    }
}

RUNTIME_CONFIGURATION = collections.ChainMap(RUNTIME_DEFAULTS)

class Configuration():
    """
        A place holder for a singleton configuration object.
    """

    configuration_lock = threading.RLock()
   
    _instance = None
    _initialize_gate = None

    def __new__(cls):
        """
            Constructs new instances of the Configuration object.
        """
        if cls._instance is None:
            cls._instance = super(Configuration, Configuration).__new__(Configuration)
            # Put any initialization here.
        return cls._instance

    def __init__(self):
        """
            Creates an instance or reference to the :class:`Configuration` singleton object.  On the first call to this
            constructor the :class:`Configuration` object is initialized and the configuration is loaded.
        """

        thisType = type(self)

        self.configuration_lock.acquire()
        try:

            if thisType._initialize_gate is None:
                thisType._initialize_gate = threading.Event()
                thisType._initialize_gate.clear()

                # We don't need to hold the landscape lock while initializing
                # the Landscape because no threads calling the constructor can
                # exit without the landscape initialization being finished.
                self.configuration_lock.release()

                try:
                    self._initialize()
                finally:
                    self.configuration_lock.acquire()

            else:

                # Don't hold the landscape like while we wait for the
                # landscape to be initialized
                self.configuration_lock.release()
                try:
                    # Because the landscape is a global singleton and because
                    # we were not the first thread to call the contructor, wait
                    # for the first calling thread to finish initializing the
                    # Landscape before we return and try to use the returned
                    # Landscape reference
                    self._initialize_gate.wait()
                finally:
                    self.configuration_lock.acquire()
        finally:
            self.configuration_lock.release()

        return

    def _initialize(self):

        self._initialize_gate.set()

        return