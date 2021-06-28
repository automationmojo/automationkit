"""
    This is a working copy of what I envision a code generated execution sequence document might look like.
    The general concept here is that if you generate a flat test execution sequence and run it, then it might
    make debugging the setup, teardown, and execution of tests easier.

    We are basically unrolling the iterators that would normally be used to execute a series of tests.  The execution
    sequence file would be available in the output folder along with the logs and such as an artifact of the test run.
"""
import logging

from akit.xlogging.foundations import getAutomatonKitLogger

from akit.testing.testplus.testgroup import TestGroup

logger = getAutomatonKitLogger()

def scope_tests(sequencer):
    with TestGroup("tests") as tg:

        # Importing the resource functions that were used to declare
        # wellknow parameters for this module execution function
        from testorg.integrations.automationpod import automation_pod

        # Initialize all of the integrations
        apod = automation_pod()

        scope_tests_hometheater(sequencer, apod)

    return

def scope_tests_hometheater(sequencer, apod):

    with TestGroup("tests.hometheater") as tg:

        # Importing the resource functions that were used to declare
        # wellknow parameters for this module execution function
        from testorg.rooms.hometheater import hometheater_room
        from testorg.services.webserver import http_content_server

        # Call the resource creation functions in order to 
        for room in hometheater_room(apod).next():
            for websrv in http_content_server().next():

                scope_tests_hometheater_dolby50(sequencer, apod, room, websrv)

    return

def scope_tests_hometheater_dolby50(sequencer, apod, room, websrv):

    with TestGroup("testplus.hometheater.dolby50") as tg:

        # Importing the resource functions local to this module execution function
        from testorg.tests.hometheater.dolby50 import random_integer

        # Importing the tests to run from this module execution function
        from testorg.tests.hometheater.dolby50 import (
            test_dolby50_a,
            test_dolby50_b
        )

        nxt_test = "test_dolby50_a"
        with sequencer.test_call_context(nxt_test, {"apod": apod, "room": room, "websrv": websrv}) as tc:
            test_dolby50_a(apod, room, websrv)

        nxt_test = "test_dolby50_b"
        with sequencer.test_scope_context() as ts:
            rint = random_integer()
            with sequencer.test_call_context(nxt_test, {"apod": apod, "room": room, "websrv": websrv, "rint": rint}) as tc:
                test_dolby50_b(apod, room, websrv, rint)

    return

def session(sequencer):

    # If the debug flag was passed then we import pdb and
    # pause in the debugger.
    import pdb
    pdb.set_trace()

    # If the remote debug flag was passed then we setup
    # a remote debug session and pause in the debugger
    # to wait for a connection.
    import rpdb
    debugger = rpdb.Rpdb(port=12345)
    debugger.set_trace()

    with TestGroup("(session)") as tg:
        scope_tests(sequencer)
