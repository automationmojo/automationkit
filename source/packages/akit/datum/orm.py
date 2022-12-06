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
from sqlalchemy import MetaData
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

AutomationBase = declarative_base()


class RepositoryType(enum.Enum):
    """
        An enumeration that indicates the JobType of a WorkQueue item.  This indicates if a
        work item is a global work item available for execution on any qualified work site or
        if it is a local work item which is meant to execute locally.
    """
    GitHub = 1

class WorkQueueJobType(enum.Enum):
    """
        An enumeration that indicates the JobType of a WorkQueue item.  This indicates if a
        work item is a global work item available for execution on any qualified work site or
        if it is a local work item which is meant to execute locally.
    """
    Local = 1
    Global = 2

class WorkQueueState(enum.Enum):
    """
        An enumeration that indicates the JobType of a WorkQueue item.  This indicates if a
        work item is a global work item available for execution on any qualified work site or
        if it is a local work item which is meant to execute locally.
    """
    Enabled = 1
    Disabled = 2

class Repository(AutomationBase, SerializableModel):
    """
        A data modelf for storing repository information.
    """

    __tablename__ = "repository"

    id = Column('repo_id', BigInteger, primary_key=True)
    name = Column('repo_name', VARCHAR(128), nullable=False)
    url = Column('repo_repository', VARCHAR(2048), nullable=False)
    repotype = Column('repo_type', Enum(RepositoryType), nullable=False)
    repoconf = Column('repo_conf', TEXT, nullable=False)

class Branch(AutomationBase, SerializableModel):
    """
        A data model for storing source branch information.
    """

    __tablename__ = "branch"

    id = Column('branch_id', BigInteger, primary_key=True)
    name = Column('branch_name', VARCHAR(128), nullable=False)
    owner = Column('branch_owner', VARCHAR(128), nullable=False)

    repo_id = Column('repo_id', BigInteger, ForeignKey(Repository.id))

class BuildResult(AutomationBase, SerializableModel):
    """
        A data model for storing build information.
    """

    __tablename__ = "build_result"

    id = Column('build_id', BigInteger, primary_key=True)
    name = Column('build_name', VARCHAR(128), nullable=False)
    start = Column('build_start', DateTime, nullable=False)
    stop = Column('build_stop', DateTime, nullable=False)
    change = Column('build_change', VARCHAR(128), nullable=False)
    
    branch_id = Column('branch_id', BigInteger, ForeignKey(Branch.id))

class BuildByProduct(AutomationBase, SerializableModel):
    """
        A data mode for linking build byproducts to build
    """
    __tablename__ = "build_byproduct"

    id = Column('byprod_id', BigInteger, primary_key=True)
    product = Column('byprod_product', VARCHAR(128), nullable=False)
    arch = Column('byprod_arch', VARCHAR(128), nullable=False)
    buildno = Column('byprod_buildno', VARCHAR(128), nullable=False)
    flavor = Column('byprod_flavor', VARCHAR(128), nullable=False)
    result_url = Column('byprod_result_url', VARCHAR(2048), nullable=False) 
    
    bldjob_id = Column('bldjob_id', BigInteger, ForeignKey(BuildResult.id))

class User(AutomationBase, SerializableModel):
    """
        A data model for the minimal amount of User information to store
        for relating automation data to an enterprise user.
    """

    __tablename__ = 'user'

    id = Column('user_id', VARCHAR(40), primary_key=True)
    firstName = Column('user_firstName', VARCHAR(40), nullable=False)
    lastName = Column('user_lastName', VARCHAR(40), nullable=False)
    email = Column('user_email', VARCHAR(128), nullable=False)
    login = Column('user_login', VARCHAR(128), nullable=False)
    ownertag = Column('user_ownertag', VARCHAR(40), nullable=True)

class WorkQueue(AutomationBase, SerializableModel):
    """
        A data model for a
    """
    __tablename__ = 'work_queue'
    
    id = Column('queue_id', BigInteger, primary_key=True, autoincrement=True)
    name = Column('queue_name', String(128), nullable=False)
    description = Column('queue_desc', TEXT, nullable=False)
    state = Column('queue_state', Enum(WorkQueueState), nullable=False)

class WorkPacket(AutomationBase, SerializableModel):
    """
        A data model for a WorkPacket(s) and the work items that are part of a work queue.
    """
    __tablename__ = 'work_packet'
    
    id = Column('wkpack_id', BigInteger, primary_key=True, autoincrement=True)

    jtype = Column('wkpk_jtype', Enum(WorkQueueJobType), nullable=False)
    title =  Column('wkpk_title', String(1024), nullable=False)
    description = Column('wkpk_description', Text, nullable=False)
    branch =  Column('wkpk_branch', String(1024), nullable=True)
    build =  Column('wkpk_build', String(1024), nullable=True)
    flavor =  Column('wkpk_flavor', String(1024), nullable=True)
    ownertag = Column('wkpk_ownertag', VARCHAR(40), nullable=True)
    added = Column('wkpk_added', DateTime, nullable=False)
    start = Column('wkpk_start', DateTime, nullable=True)
    stop = Column('wkpk_stop', DateTime, nullable=True)
    progress = Column('wkpk_progress', Float, default=0.0)
    status = Column('wkpk_status', String(50), nullable=False)
    packet = Column('wkpk_packet', TEXT, nullable=False)

    queue_id = Column('queue_id', BigInteger, ForeignKey(WorkQueue.id), nullable=False)
    user_id = Column('user_id', VARCHAR(40), ForeignKey(User.id), nullable=False)


class FeatureGroup(AutomationBase, SerializableModel):
    """
        A data model for storing information about feature groups.
    """
    __tablename__ = 'feature_group'
    
    id = Column('lsscan_id', BigInteger, primary_key=True)
    name = Column('fg_name', VARCHAR(256), nullable=False)
    description = Column('fg_description', TEXT, nullable=False)

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

    lscape_id = Column('lsdesc_id', BigInteger, ForeignKey(Landscape.id))

class TestJob(AutomationBase, SerializableModel):
    """
        A data model for storing information about test jobs and
        user and feature group associations with a given test job.
    """
    __tablename__ = 'test_job'
    
    id = Column('job_id', VARCHAR(40), primary_key=True)
    title =  Column('job_title', VARCHAR(1024), nullable=False)
    description = Column('job_description', Text, nullable=False)

    owner_fg_id = Column('owner_fg_id', BigInteger, ForeignKey(FeatureGroup.id), nullable=True)

class TestJobRun(AutomationBase, SerializableModel):
    """
        A data model for a TestJob run.
    """

    __tablename__ = 'test_job_run'
    
    id = Column('tjr_id', BigInteger, primary_key=True)
    instance = Column('tjr_instance', UUIDType, nullable=False)
    branch =  Column('tjr_branch', VARCHAR(1024), nullable=True)
    build =  Column('tjr_build', VARCHAR(1024), nullable=True)
    flavor =  Column('tjr_flavor', VARCHAR(1024), nullable=True)
    ownertag = Column('wkpk_ownertag', VARCHAR(40), nullable=True)
    start = Column('tjr_start', DateTime, nullable=False)
    stop = Column('tjr_stop', DateTime, nullable=True)
    detail = Column('tjr_detail', JSON, nullable=True)

    job_id = Column('job_id', VARCHAR(40), ForeignKey(TestJob.id), nullable=False)
    user_id = Column('user_id', VARCHAR(40), ForeignKey(User.id), nullable=False)

    lscape_id = Column('lsdesc_id', BigInteger, ForeignKey(Landscape.id), nullable=True)
    lsscan_id = Column('lsscan_id', BigInteger, ForeignKey(LandscapeScan.id), nullable=True)
    fg_id = Column('fg_id', BigInteger, ForeignKey(FeatureGroup.id), nullable=True)

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

    testjob_id = Column('tj_id', VARCHAR(40), ForeignKey(TestJob.id))

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

    testjob_id = Column('tj_id', VARCHAR(40), ForeignKey(TestJob.id))

class FeatureGroupMembership(AutomationBase, SerializableModel):
    """
        A data model for associating FeatureGroup(s) to Users(s)
    """
    __tablename__ = "feature_group_membership"
    
    fg_id = Column('fg_id', BigInteger, ForeignKey(FeatureGroup.id), primary_key=True)
    user_id = Column('user_id', VARCHAR(40), ForeignKey(User.id), primary_key=True)

    join_date = Column('fgm_join_date', DateTime, nullable=False)
    departure_date = Column('fgm_departure_date', DateTime, nullable=True)

