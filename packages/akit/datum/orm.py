"""
.. module:: orm
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains the ORM associated with the akit database storage

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

import enum
import json

from sqlalchemy import BigInteger, Column, DateTime, Enum, Float, String, Text, VARCHAR, ForeignKey, TEXT
from sqlalchemy import inspect
from sqlalchemy.types import JSON

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_utils.types.uuid import UUIDType


class SerializableModel:
    """
        Mixin style class that adds serialization to data model objects.
    """

    def to_dict(self):
        """
            Iterates the formal data attributes of a model and outputs a dictionary
            with the data based on the model.
        """
        dval = {}

        model = type(self)
        mapper = inspect(model)
        for col in mapper.attrs:
            col_key = col.key
            dval[col_key] = str(getattr(self, col_key))

        return dval


    def to_json(self, indent=4):
        """
            Iterates the formal data attributes of a model and creates a dictionary
            with the data based on the model, then converts the dictionary to a
            JSON string.
        """
        model_dict = self.to_dict()
        json_str = json.dumps(model_dict, indent=indent)
        return json_str

AutomationUser = declarative_base()

class User(AutomationUser, SerializableModel):
    """
        A data model for the minimal amount of User information to store
        for relating automation data to a user.
    """

    __tablename__ = 'user'

    id = Column('user_id', VARCHAR(40), primary_key=True)
    firstName = Column('user_firstName', VARCHAR(40), nullable=False)
    lastName = Column('user_lastName', VARCHAR(40), nullable=False)
    email = Column('user_email', VARCHAR(128), nullable=False)
    login = Column('user_login', VARCHAR(128), nullable=False)

AutomationBase = declarative_base()

class TestJob(AutomationBase, SerializableModel):
    """
        A data model for a TestJob run.
    """

    __tablename__ = 'test_job'

    id = Column('tj_id', BigInteger, primary_key=True)
    title =  Column('tj_title', VARCHAR(1024), nullable=False)
    description = Column('tj_description', Text, nullable=False)
    instance = Column('tj_instance', UUIDType, nullable=False)
    branch =  Column('tj_branch', VARCHAR(1024), nullable=True)
    build =  Column('tj_build', VARCHAR(1024), nullable=True)
    flavor =  Column('tj_flavor', VARCHAR(1024), nullable=True)
    start = Column('tj_start', DateTime, nullable=False)
    stop = Column('tj_stop', DateTime, nullable=True)
    detail = Column('tj_detail', JSON, nullable=True)

    lscape_id = Column('lsdesc_id', BigInteger, ForeignKey("landscape.lsdesc_id"), nullable=True)
    lsscan_id = Column('lsscan_id', BigInteger, ForeignKey("landscape_scan.lsscan_id"), nullable=True)

class Landscape(AutomationBase, SerializableModel):
    """
        A data model that describes a test landscape.
    """
    __tablename__ = 'landscape'

    id = Column('lsdesc_id', BigInteger, primary_key=True)
    name =  Column('lsdesc_name', VARCHAR(1024), nullable=False)
    detail = Column('lsdesc_detail', JSON, nullable=False)

class LandscapeScan(AutomationBase, SerializableModel):
    """
        A data model that describes the results of a test landscape scan.
    """
    __tablename__ = 'landscape_scan'

    id = Column('lsscan_id', BigInteger, primary_key=True)
    name =  Column('lsscan_name', VARCHAR(1024), nullable=False)
    detail = Column('lsscan_detail', JSON, nullable=False)

    lscape_id = Column('lsdesc_id', BigInteger, ForeignKey("landscape.lsdesc_id"))

class TestResult(AutomationBase, SerializableModel):
    """
        A data model for a TestResult node that is part of a test result tree.
    """
    __tablename__ = 'test_result'

    id = Column('tstr_id', BigInteger, primary_key=True)
    name =  Column('tstr_name', VARCHAR(1024), nullable=False)
    extname = Column('tstr_extname', VARCHAR(1024), nullable=True)
    parameters = Column('tstr_parameters', Text, nullable=True)
    instance = Column('tstr_instance', UUIDType, nullable=False)
    parent = Column('tstr_parent', UUIDType, nullable=True)
    rtype = Column('tstr_rtype', String(50), nullable=False)
    result = Column('tstr_result', String(50), nullable=False)
    start = Column('tstr_start', DateTime, nullable=False)
    stop = Column('tstr_stop', DateTime, nullable=True)
    detail = Column('tstr_detail', JSON, nullable=True)

    testjob_id = Column('tj_id', BigInteger, ForeignKey("test_job.tj_id"))

class TestResultContainer(AutomationBase, SerializableModel):
    """
        A data model for a TestResultContainer node that is part of a test result tree.  The
        TestResultContainer node serves as a parent and container for individual result based
        nodes.
    """
    __tablename__ = 'test_result_container'

    id = Column('tstrcont_id', BigInteger, primary_key=True)
    name =  Column('tstrcont_name', VARCHAR(1024), nullable=False)
    instance = Column('tstrcont_instance', UUIDType, nullable=False)
    parent = Column('tstrcont_parent', UUIDType, nullable=True)
    rtype = Column('tstrcont_rtype', String(50), nullable=False)

    testjob_id = Column('tj_id', BigInteger, ForeignKey("test_job.tj_id"))


AutomationQueue = declarative_base()

class WorkQueueJobType(enum.Enum):
    """
        An enumeration that indicates the JobType of a WorkQueue item.  This indicates if a
        work item is a global work item available for execution on any qualified work site or
        if it is a local work item which is meant to execute locally.
    """
    Local = 1
    Global = 2

class WorkPacket(AutomationQueue, SerializableModel):
    """
        A data model for a WorkQueue and the work items that are part of a work queue.
    """
    __tablename__ = 'work_queue'

    id = Column('wkpack_id', BigInteger, primary_key=True, autoincrement=True)

    jtype = Column('wkpk_jtype', Enum(WorkQueueJobType), nullable=False)
    title =  Column('wkpk_title', String(1024), nullable=False)
    description = Column('wkpk_description', Text, nullable=False)
    branch =  Column('wkpk_branch', String(1024), nullable=True)
    build =  Column('wkpk_build', String(1024), nullable=True)
    flavor =  Column('wkpk_flavor', String(1024), nullable=True)
    added = Column('wkpk_added', DateTime, nullable=False)
    start = Column('wkpk_start', DateTime, nullable=True)
    stop = Column('wkpk_stop', DateTime, nullable=True)
    progress = Column('wkpk_progress', Float, default=0.0)
    status = Column('wkpk_status', String(50), nullable=False)
    packet = Column('wkpk_packet', TEXT, nullable=True)

    result_id = Column('result_id', String(64), nullable=False)
    user_id = Column('user_id', BigInteger, nullable=False)
