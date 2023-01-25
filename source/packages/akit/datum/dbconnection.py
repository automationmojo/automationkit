
from typing import List

import os

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine as BaseEngine

from akit.environment.contextpaths import ContextPaths
from akit.exceptions import AKitConfigurationError, AKitNotOverloadedError
from akit.interop.credentials.basiccredential import BasicCredential
from akit.interop.credentials.credentialmanager import CredentialManager

from akit.xlogging.foundations import getAutomatonKitLogger

logger = getAutomatonKitLogger()

class DatabaseConnectionFactory:
    def create_engine(self, *, dbname=None, echo=True) -> BaseEngine:
        errmsg = "The 'create_engine' method must be overloaded by 'DatabaseConnectionFactory' derived types."
        raise AKitNotOverloadedError(errmsg)

class BasicDatabaseConnectionFactory(DatabaseConnectionFactory):

    def __init__(self, profile_name, *, conntype: str, dbtype:str, credential: str, dbname: str=None):
        self.profile_name = profile_name
        self.conntype = conntype
        self.dbtype = dbtype
        self.dbname = dbname
        self.credential = credential
        return

    def create_engine(self, *, dbname=None, echo=True) -> BaseEngine:
        # TODO: Implement pipe based DB connection engine creation
        return

class BasicTcpDatabaseConnectionFactory(DatabaseConnectionFactory):

    def __init__(self, profile_name, *, conntype: str, dbtype:str, host: str, port: int, credential: str, dbname: str=None):
        self.profile_name = profile_name
        self.conntype = conntype
        self.dbtype = dbtype
        self.host = host
        self.port = port
        self.credential = credential
        self.dbname = dbname
        return

    def create_engine(self, *, dbname=None, echo=True) -> BaseEngine:

        # If the database type we are creating an engine for is postgresql, make sure
        # we can import all of the postgresql dependencies.
        if self.dbtype == 'postgresql':
            try:
                import psycopg2
            except ImportError:
                errmsg_lines = [
                    "In order to create a postgresql database engine, you must install the following dependencies.",
                    "DEPENDENCIES",
                    "    psycopg2"
                ]
                errmsg = os.linesep.join(errmsg_lines)
                raise AKitConfigurationError(errmsg)

        if dbname is None and self.dbname is not None:
            dbname = self.dbname

        if dbname is None:
            warnmsg = "BasicTcpDatabaseConnectionFactory.create_engine: dbname was None."
            logger.warn(warnmsg)

        credmgr = CredentialManager()

        cred = credmgr.credentials[self.credential]
        if isinstance(cred, BasicCredential):
            connstr = '%s+psycopg2://%s:%s@%s:%d/%s' % (
                self.dbtype, cred.username, cred.password, self.host, self.port, dbname)
            dbengine = create_engine(connstr, echo=echo)

        return dbengine

database_connection_factories = {}

def lookup_database_connection_factory(conn_profile: str):

    global database_connection_factories

    conn_factory = None

    if conn_profile in database_connection_factories:
        conn_factory = database_connection_factories[conn_profile]
    else:
        from akit.environment.context import Context

        ctx = Context()
        
        conn_info = None

        rcdatabases = ctx.lookup(ContextPaths.DATABASES)
        if rcdatabases is not None and conn_profile in rcdatabases:
            conn_info = rcdatabases[conn_profile].value
        else:
            from akit.wellknown.singletons import LandscapeSingleton

            lscape = LandscapeSingleton()
            lsdatabases = lscape.databases
            if lsdatabases is not None and conn_profile in lsdatabases:
                conn_info = lsdatabases[conn_profile]

        if conn_info is not None:
            if "conntype" in conn_info:
                conntype = conn_info["conntype"].lower()
                if conntype == "basic":
                    conn_factory = BasicDatabaseConnectionFactory(conn_profile, **conn_info)
                elif conntype == "basic-tcp":
                    conn_factory = BasicTcpDatabaseConnectionFactory(conn_profile, **conn_info)
                else:
                    errmsg = "Unknown database connection type. connection={} conntype={}".format(
                        conn_profile, conntype)
                    raise AKitConfigurationError(errmsg)

                database_connection_factories[conn_profile] = conn_factory
            else:
                errmsg = "Database connection entries must have a 'conntype' entry. connection={}".format(
                    conn_profile
                )
                raise AKitConfigurationError(errmsg)
        else:
            errmsg = "Database connection not found. connection={}".format(
                conn_profile
            )
            raise AKitConfigurationError(errmsg)

    return conn_factory