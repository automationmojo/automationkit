"""
    This is a working copy of what I envision a code generated execution sequence document might look like.
    The general concept here is that if you generate a flat test execution sequence and run it, then it might
    make debugging the setup, teardown, and execution of tests easier.

    We are basically unrolling the iterators that would normally be used to execute a series of tests.  The execution
    sequence file would be available in the output folder along with the logs and such as an artifact of the test run.
"""
from akit.testing.testplus.testgroup import TestGroup

from testorg.integrations.automationpod import automation_pod

apod = automation_pod()

def scope_tests(parent):
    with TestGroup("tests") as tg:

        scope_tests_hometheater(tg)

    return

def scope_tests_hometheater(parent):
    global apod

    with TestGroup("tests.hometheater") as tg:

        from testorg.integrations.hometheater import hometheater_room
        from testorg.integrations.webserver import http_content_server

        room = hometheater_room(apod)
        websrv = http_content_server()

        scope_tests_hometheater_dolby50(tg, room, websrv)

    return

def scope_tests_hometheater_dolby50(parent, room, websrv):
    with TestGroup("testplus.hometheater.dolby50") as tg:

        from testorg.tests.hometheater.dolby50 import [
            test_dolby50
        ]

        test_dolby50(room, websrv)

    return

def session():

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

        try:
            # Initialize all of the integrations
            pass

            scope_tests(tg)
        finally:
            # Perform de-integration releasing any resources
            # being held
            pass

session()
