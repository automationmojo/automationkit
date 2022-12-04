"""
.. module:: dbio
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Contains helper functions for working with specific databases

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

import contextlib
import traceback

from akit.exceptions import AKitConfigurationError

from akit.datum.orm import AutomationBase

from akit.datum.dbconnection import DatabaseConnectionFactory, lookup_database_connection_factory

def database_exists(conn_factory: DatabaseConnectionFactory, dbname: str):
    """
        Checks to see if the specified database exists.
    """
    engine = conn_factory.create_engine(dbname="postgres", echo=True)
    result = engine.execute("SELECT 1 AS result FROM pg_database WHERE datname='%s'" % dbname)
    return result.rowcount > 0

def database_create(conn_factory: DatabaseConnectionFactory, dbname):
    """
        Creates the specified database.
    """
    engine = conn_factory.create_engine(dbname="postgres", echo=True)

    conn = engine.connect()
    try:
        conn.connection.set_isolation_level(0)
        result = conn.execute("CREATE DATABASE %s" % dbname)
    except Exception as xcpt:
        print(traceback.format_exc())
        raise
    finally:
        conn.close()

    return

def create_automation_database(db_profile_name: str):
    """
        Creates the 'automation' database.
    """
    dbname = "automation"
    conn_factory = lookup_database_connection_factory(db_profile_name)

    if not database_exists(conn_factory, dbname):
        database_create(conn_factory, dbname)

    engine = conn_factory.create_engine(dbname=dbname, echo=True)

    # TODO: Solidify the data model and the metadata base used
    # to create the database
    AutomationBase.metadata.create_all(engine, checkfirst=True)

    return

def open_automation_database(db_profile_name: str):
    """
        Opens the 'automation' postgresql database.
    """
    dbname = 'automation'

    conn_factory = lookup_database_connection_factory(db_profile_name)
    if conn_factory is None:
        errmsg = "'open_automation_database' could not get a connection factory for profile={}".format(
            db_profile_name
        )
        raise AKitConfigurationError(errmsg)

    engine = conn_factory.create_engine(dbname=dbname, echo=True)

    return engine

def reset_automation_database(db_profile_name: str):
    """
        Reset the 'automation' database.
    """
    dbname = "automation"
    conn_factory = lookup_database_connection_factory(db_profile_name)

    if database_exists(conn_factory, dbname):
    
        engine = conn_factory.create_engine(dbname=dbname, echo=True)

        with contextlib.closing(engine.connect()) as con:
            trans = con.begin()
            con.execute('TRUNCATE {} RESTART IDENTITY;'.format(
                ','.join(table.name 
                        for table in reversed(AutomationBase.metadata.sorted_tables))))
            trans.commit()

    return

