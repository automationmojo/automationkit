"""
.. module:: topologydescription
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`TopologyDescription` class.

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

import os
import shutil
import traceback
import yaml

from akit.exceptions import AKitConfigurationError, AKitRuntimeError
from akit.environment.context import Context
from akit.xlogging.foundations import getAutomatonKitLogger

if TYPE_CHECKING:
    from akit.integration.landscaping.landscape import Landscape

class TopologyDescription:
    """
        The base class for all derived :class:`TopologyDescription` objects.  The
        :class:`TopologyDescription` is used to load a description of the overlayed
        relationships between the entities in the test landscape.
    """

    def load(self, topology_file: str, log_to_directory: Optional[str]=None):
        """
            Loads and validates the landscape description file.
        """
        logger = getAutomatonKitLogger()

        topology_info = None


        with open(topology_file, 'r') as tf:
            tfcontent = tf.read()
            topology_info = yaml.safe_load(tfcontent)

        if log_to_directory is not None:
            try:
                topology_file_basename = os.path.basename(topology_file)
                topology_file_basename, topology_file_ext = os.path.splitext(topology_file_basename)

                topology_file_copy = os.path.join(log_to_directory, "{}-declared{}".format(topology_file_basename, topology_file_ext))
                shutil.copy2(topology_file, topology_file_copy)
            except Exception as xcpt:
                err_msg = "Error while logging the topology file (%s)%s%s" % (
                    topology_file, os.linesep, traceback.format_exc())
                raise AKitRuntimeError(err_msg) from xcpt

        errors, warnings = self.validate_topology(topology_info)

        if len(errors) > 0:
            errmsg_lines = [
                "ERROR Topology validation failures:"
            ]
            for err in errors:
                errmsg_lines.append("    %s" % err)

            errmsg = os.linesep.join(errmsg_lines)
            raise AKitConfigurationError(errmsg) from None

        if len(warnings) > 0:
            for wrn in warnings:
                logger.warn("Topology Configuration Warning: (%s)" % wrn)

        return topology_info

    def validate_topology(self, topology_info):
        """
            Validates the landscape description file.
        """
        errors = []
        warnings = []

        return errors, warnings

