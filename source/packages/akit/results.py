
"""
.. module:: results
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`TaskBase` object which is used as the base.

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

from typing import Any, Dict, List, Optional

import collections
import enum
import json
import os
import time

from akit.xtime import format_time_with_fractional

class ResultCode(enum.IntEnum):
    """
        Enumeration that summarizes a result.
    """
    UNSET = 0
    PASSED = 1
    SKIPPED = 2
    ERRORED = 3
    FAILED = 4
    UNKOWN = 5

class ResultType(enum.IntEnum):
    """
        Enumeration to mark the type of result.
    """
    JOB = 0
    PACKAGE = 1
    SCOPE = 2
    TASK_CONTAINER = 3
    TASK = 4
    TEST_CONTAINER = 5
    TEST = 6
    STEP_CONATINER = 7
    STEP = 8

class ResultNode:
    """
        The :class:`ResultNode` object marks a result node that contains results from a task, test or step in a result tree.  The
        result trees only store results that contain result data not associated with the hierarchy of the results.  The result tree
        does not contain results that can be computed by analyzing the relationship of the nodes in the tree.  The nodes that are
        computed are :class:`ResultContainer` instances and do not contain instance result data.
    """
    def __init__(self, inst_id: str, name: str, monikers: List[str], pivots: Dict[str, Any], result_type: ResultType, result_code: ResultCode = ResultCode.UNSET, parent_inst: Optional[str] = None):
        """
            Initializes an instance of a :class:`ResultNode` object that represent the information associated with
            a specific result in a result tree.

            :param inst_id: The unique identifier to link this result container with its children.
            :param name: The name of the result container.
            :param monikers: The names of parameters used to extend the result name.
            :param pivots: A tuple of data pivots used for result comparisons.
            :param result_type: The type :class:`ResultType` type code of result container.
            :param result_code: The result code to initialize the result node to.
            :param parent_inst: The unique identifier fo this result nodes parent.
        """
        super().__init__()

        self._inst_id = inst_id
        self._name = name
        self._monikers = monikers
        self._pivots = pivots
        self._parent_inst = parent_inst
        self._result_code = result_code
        self._result_type = result_type
        self._start = time.time()
        self._stop = None
        self._errors = []
        self._failures = []
        self._warnings = []
        self._reason = None
        self._bug = None
        self._docstr = None
        return

    @property
    def parent_inst(self):
        """
            The unique identifier fo this result nodes parent.
        """
        return self._parent_inst

    @property
    def result_code(self):
        """
            The type :class:`ResultType` type code of result container.
        """
        return self._result_code

    @property
    def inst_id(self):
        """
            The unique identifier to link this result container with its children.
        """
        return self._inst_id

    @property
    def name(self):
        """
            The name of the result item.
        """
        return self._name

    @property
    def pivots(self):
        """
            The name of the result pivots.
        """
        return self._pivots

    @property
    def result_type(self):
        """
            The :class:`ResultType` code associated with this result node.
        """
        return self._result_type

    def add_error(self, err_lines: List[str]):
        """
            Adds error trace lines for a single error to this result node.
        """
        trim_lines = []
        for nline in err_lines:
            nline = nline.rstrip()
            nlindex = nline.find(os.linesep)
            if nlindex > -1:
                trim_lines.append(nline[:nlindex])
                trim_lines.append(nline[nlindex + 1:])
            else:
                trim_lines.append(nline)
        self._errors.append(trim_lines)
        return

    def add_failure(self, fail_lines: List[str]):
        """
            Adds failure trace lines for a single failure to this result node.
        """
        trim_lines = []
        for nline in fail_lines:
            nline = nline.rstrip()
            nlindex = nline.find(os.linesep)
            if nlindex > -1:
                trim_lines.append(nline[:nlindex])
                trim_lines.append(nline[nlindex + 1:])
            else:
                trim_lines.append(nline)
        self._failures.append(trim_lines)
        return

    def add_warning(self, warn_lines: List[str]):
        """
            Adds warning trace lines for a single warning to this result node.
        """
        trim_lines = []
        for nline in warn_lines:
            nline = nline.rstrip()
            nlindex = nline.find(os.linesep)
            if nlindex > -1:
                trim_lines.append(nline[:nlindex])
                trim_lines.append(nline[nlindex + 1:])
            else:
                trim_lines.append(nline)
        self._warnings.append(trim_lines)
        return

    def set_documentation(self, docstr):
        """
            Sets the documentation string associated with this result node.
        """
        self._docstr = docstr
        return

    def finalize(self):
        """
            Finalizes the :class:`ResultCode` code for this result node based on whether
            there were any errors or failures added to the node.
        """
        self._stop = time.time()

        if len(self._failures) > 0:
            self._result_code = ResultCode.FAILED
        elif len(self._errors) > 0:
            self._result_code = ResultCode.ERRORED
        elif self._result_code == ResultCode.UNSET:
            self._result_code = ResultCode.UNKOWN

        return

    def mark_passed(self):
        """
            Marks this result with a :class:`ResultCode` of ResultCode.PASSED
        """
        self._result_code = ResultCode.PASSED
        return

    def mark_skip(self, reason: str, bug: str):
        """
            Marks this result with a :class:`ResultCode` of ResultCode.SKIPPED

            :param reason: The reason the task or test this result is associated with was skipped.
        """
        self._reason = reason
        self._bug = bug
        self._result_code = ResultCode.SKIPPED
        return

    def to_dict(self) -> collections.OrderedDict:
        """
            Converts the result node instance to an :class:`collections.OrderedDict` object.
        """
        detail_items = [
            ("errors", self._errors),
            ("failures", self._failures),
            ("warnings", self._warnings)
        ]

        if self._reason is not None:
            detail_items.append(("reason", self._reason))
        
        if self._bug is not None:
            detail_items.append(("bug", self._bug))
        

        detail = collections.OrderedDict(detail_items)

        if self._docstr is not None:
            detail["documentation"] =  self._docstr

        start_datetime = format_time_with_fractional(self._start)
        stop_datetime = format_time_with_fractional(self._stop)

        rninfo = collections.OrderedDict([
            ("name", self._name),
            ("monikers", self._monikers),
            ("pivots", self._pivots),
            ("instance", self._inst_id),
            ("parent", self._parent_inst),
            ("rtype", self._result_type.name),
            ("result", self._result_code.name),
            ("start", start_datetime),
            ("stop", stop_datetime),
            ("detail", detail)
        ])

        return rninfo

    def to_json(self) -> str:
        """
            Converts the result node instance to JSON format.
        """
        rninfo = self.to_dict()

        rnstr = json.dumps(rninfo, indent=4)

        return rnstr

class ResultContainer:
    """
        The :class:`ResultContainer` instances are container nodes that are used to link result nodes in the
        result tree.  The :class:`ResultContainer` nodes do not contain result data but link data so the data can
        be computed on demand.
    """
    def __init__(self, inst_id: str, name: str, result_type, parent_inst: Optional[str] = None):
        """
            Creates an instance of a result container.

            :param inst_id: The unique identifier to link this result container with its children.
            :param name: The name of the result container.
            :param result_type: The type :class:`ResultType` type code of result container.
            :param parent_inst: The unique identifier fo this result nodes parent.
        """
        super().__init__()

        self._inst_id = inst_id
        self._name = name
        self._parent_inst = parent_inst
        self._result_type = result_type
        return

    @property
    def parent_inst(self) -> str:
        """
            The unique identifier fo this result nodes parent.
        """
        return self._parent_inst

    @property
    def inst_id(self) -> str:
        """
            The unique identifier to link this result container with its children.
        """
        return self._inst_id

    @property
    def name(self) -> str:
        """
            The name of the result container.
        """
        return self._name

    @property
    def result_type(self) -> ResultType:
        """
            The type :class:`ResultType` type code of result container.
        """
        return self._result_type

    def to_dict(self) -> collections.OrderedDict:
        """
            Converts the result container instance to an :class:`collections.OrderedDict` object.
        """
        rcinfo = collections.OrderedDict([
            ("name", self._name),
            ("instance", self._inst_id),
            ("parent", self._parent_inst),
            ("rtype", self._result_type.name)
        ])

        return rcinfo

    def to_json(self) -> str:
        """
            Converts the result container instance to JSON format.
        """
        rcinfo = self.to_dict()

        rcstr = json.dumps(rcinfo, indent=4)

        return rcstr
