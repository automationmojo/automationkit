"""
.. module:: testjob
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is contains the :class:`TestJob` class which is utilized for each test
        run as the parent container for all test results.

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

from typing import List

import os
import traceback

from akit.environment.context import ContextUser

from akit.recorders import JsonResultRecorder
from akit.environment.variables import AKIT_VARIABLES
from akit.wellknown.singletons import LandscapeSingleton
from akit.xformatting import CommandOutputFormat

from akit.testing.testplus.testsequencer import TestSequencer

from akit.xdebugger import WELLKNOWN_BREAKPOINTS, debugger_wellknown_breakpoint_entry

class TestJob(ContextUser):
    """
        The :class:`TestJob` spans the execution of all :class:`TestPack` and organizes the
        flow of execution of test packs.  It allows for the sequencing of the execution of test
        packs so as to optimize the time test runs spend performing setup and tearnown tasks.  This
        allows for the optimization of infrastructure resources.

        * Single Instance
        * Setup Test Landscape
        * Jobs have an expected number of tests based
        * Collects and organizes results from all the :class:`TestPack` runs

        * Can be used to customize the sequencing of :class:`TestPack` runs.
    """

    title = "" # Friendly name for the test job
    description = "" # Description of the job

    includes = None # The test packs or tests that are included in this TestJob
    excludes = None # The tests that are to be excluded from this TestJob
    metafilters = None

    _instance = None

    def __new__(cls, *_args, **_kwargs):
        """
            Creates an instance of a TestJob and then returns that instance of the TestJob for all subsequent
            calls to create test Job instances.
        """
        if cls._instance is None:
            cls._instance = super(TestJob, cls).__new__(cls)
        return cls._instance

    def __init__(self, logger, testroot, includes=None, excludes=None, metafilters=None, test_module=None, parser=None,
                 apod=None, branch=None, build=None, flavor=None):
        """
            Constructor for a :class:`TestJob`.  It initializes the member variables based on the parameters passed
            from the entry point function and the class member data declared on :class:`TestJob` derived classes.
        """
        self._logger = logger
        self._testroot = testroot

        if self.includes is None:
            self.includes = includes
            self.excludes = excludes

        self.metafilters = metafilters

        self._test_module = test_module
        self._parser = parser
        self._runid = None
        self._starttime = None

        self._test_results_dir = None
        self._result_filename = None
        self._summary_filename = None
        self._import_errors_filename = None

        self._testpacks = None

        self._apod = apod
        if apod is None:
            self._apod = AKIT_VARIABLES.AKIT_APOD_NAME

        self._branch = branch
        if branch is None:
            self._branch = AKIT_VARIABLES.AKIT_BUILD_BRANCH

        self._build = build
        if build is None:
            self._build = AKIT_VARIABLES.AKIT_BUILD_NAME

        self._flavor = flavor
        if flavor is None:
            self._flavor = AKIT_VARIABLES.AKIT_BUILD_FLAVOR

        self._import_errors = []

        return

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        self.finalize()
        return False

    @property
    def import_errors(self):
        return self._import_errors

    def begin(self):
        """
            Called at the beginning of a test job in order to setup the recording of test results.
        """

        env = self.context.lookup("/environment")

        self._test_results_dir = env["output_directory"]
        self._starttime = env["starttime"]
        self._runid = env["runid"]

        self._result_filename = os.path.join(self._test_results_dir, "testrun_results.jsos")
        self._summary_filename = os.path.join(self._test_results_dir, "testrun_summary.json")
        self._import_errors_filename = os.path.join(self._test_results_dir, "import_errors.jsos")
        self._testrun_sequence_filename = os.path.join(self._test_results_dir, "testrun_sequence.py")
        
        return

    def execute(self):
        """
            Runs the tests that are included in the given :class:'TestPack'.
        """
        result_code = 0

        with self._create_sequencer() as tseq:
            # IMPORTANT: The ordering of the automation sequence is extremely important.  Proper
            # ordering of these steps ensures that the correct things are happening in the correct
            # order in the automation code and that we provide the ability for configuration
            # issues to be discovered as early as possible.

            env = self.context.lookup("/environment")
            debugger = env["debugger"]
            breakpoints = env["breakpoints"]

            # STEP 1: We discover the tests first so we can build a listing of the
            # Integration and Scope couplings.  We don't want to execute any test code, setup,
            # or teardown code at this point.  We want to seperate out the integration
            # code from the test code and run the integration code first so we can discover
            # integration issues independant of the test code itself.
            self._logger.section("Discovery")
            debugger_wellknown_breakpoint_entry(WELLKNOWN_BREAKPOINTS.TEST_DISCOVERY)

            count = tseq.discover(test_module=self._test_module)

            # STEP 2: Tell the sequencer to record any import errors that happened during discovery
            # of tests.  If a test file or dependent file failed to import then the test
            # will just not be included in a run and this is a type of invisible error
            # that we must plan for and highlight.
            self._import_errors.extend(tseq.import_errors)
            tseq.record_import_errors(self._import_errors_filename)

            if count > 0:

                self._logger.section("Integration Publishing")

                # Initiate contact with the TestLandscape
                landscape = LandscapeSingleton() # pylint: disable=unused-variable
                landscape.activate_configuration()

                # STEP 3: Call attach_to_framework on the sequencer to give all the couplings a chance
                # to plug themselves into the automation framework.  This allows us to only integrate
                # couplings that are being consumed by the tests AND also to only include couplings that
                # are included in the test framework.  This give the opportunity for the couplings to trigger
                # the startup of the coordinators that inter-operate with the test landscape and the
                # associated devices.
                self._logger.section("Attaching to Framework")
                tseq.attach_to_framework(landscape)

                # STEP 4: After all the couplings have had the opportunity to plug themselves into
                # the test framework, we trigger the finalization of the test landscape initialization
                self._logger.section("Finalizing Coupling Registration")
                landscape.activate_integration()

                # STEP 5: Now that we have collected all the couplings and have a preview of
                # the complexity of the automation run encoded into the coupling types collected.
                # Allow the couplings to attach to the automation environment so they can get
                # a preview of the parameters and configuration and provide us with an early
                # indicator of any parameter or configuration issues.
                #
                # This is the final step of validating all the input information to the run and
                # we are able to perform this step in the context of the integration code and
                # outside of the execution of any test code
                self._logger.section("Attaching to Environment")
                tseq.attach_to_environment(landscape)

                # STEP 6: All the couplings have had a chance to analyze the configuration
                # information and provide us with a clear indication if there are any configuration
                # issues.  Now provide the couplings with the opportunity to reach out to the
                # automation infrastructure and checkout or collect any global shared resources
                # that might be required for this automation run.
                self._logger.section("Collecting Resources")
                tseq.collect_resources()

                # STEP 7: Finalize the activation process and transition the landscape
                # to fully active where all APIs are available.
                #
                # Because the Automation Kit is a distrubuted automation test framework,
                # we want to provide an early opportunity for all the integration and scope couplings
                # to establish initial connectivity or first contact with the resources or devices
                # that are being integrated into the automation run.
                #
                # This helps to ensure the reduction of automation failure noise due to configuration
                # or environmental issues
                self._logger.section("Establishing Connectivity")
                landscape.activate_operations()

                # STEP 8: After we have established that we have good connectivity with all of the
                # test landscape devices, we then want to give the integration couplings an opportunity
                # to establish a presence of presistent functionality or services with the remote devices
                tseq.establish_presence()

                # STEP 9: Capture a pre-testrun diagnostic capture
                tseq.diagnostic_capture_pre_testrun()

                self._logger.section("Expanding Test Tree Based on Query")
                tseq.expand_test_tree_based_on_query()

                self._logger.section("Generating Test Run Sequence")
                # STEP 10: Generate the test run sequence document that will be used or the run.
                tseq.generate_testrun_sequence_document(self._testrun_sequence_filename)

                title = self.title
                runid = self._runid
                start = str(self._starttime)
                sum_file = self._summary_filename
                res_file = self._result_filename
                apod = self._apod
                branch = self._branch
                build = self._build
                flavor = self._flavor

                self._logger.section("Running Tests")
                # STEP 11: The startup phase is over, up to this point we have mostly been executing
                # integration code and configuration analysis code that is embedded into mostly class
                # level methods.
                #
                # Now we start going through all the test testpacks and tests and start instantiating
                # test scopes and instances and start executing setup, teardown and test level code
                with JsonResultRecorder(title, runid, start, sum_file, res_file, apod=apod, branch=branch, build=build, flavor=flavor) as recorder:
                    try:
                        # Traverse the execution graph
                        tseq.execute_tests(runid, recorder)

                        try:
                            # STEP 12: Capture a post-testrun diagnostic capture
                            tseq.diagnostic_capture_post_testrun()
                        except Exception:
                            err_msg = traceback.format_exc()
                            self._logger.error(err_msg)

                    finally:
                        recorder.finalize()

                        recorded_sumary = recorder.summary
                        if "result" in recorded_sumary:
                            if recorded_sumary["result"] != "PASSED":
                                result_code = -1
                        else:
                            self._logger.error("The 'result' field was not found in the recorded summary report.")
                            result_code = -1

                        # STEP 13: This is where we do any final processing and or publishing of results.
                        # We might also want to add automated bug filing here later.
                        self._logger.section("Completed Tests")

                        # Write out the test results
                        results_msg_lines = [""]
                        results_msg_lines.extend(recorder.format_lines())
                        results_msg_lines.append("")

                        results_msg = os.linesep.join(results_msg_lines)

                        self._logger.render(results_msg)

            else:
                # We didn't find any tests so display a message, and set the return code to
                # indicate an error condition
                err_msg_lines = [
                    "The include and exclude parameters specified resulted in an empty test set."
                ]

                if self.includes is not None:
                    err_msg_lines.append("INCLUDES:")
                    for nxtitem in self.includes:
                        err_msg_lines.append("    %s" % nxtitem)
                    err_msg_lines.append("")
                else:
                    err_msg_lines.append("INCLUDES: None")

                if self.excludes is not None:
                    err_msg_lines.append("EXCLUDES:")
                    for nxtitem in self.excludes:
                        err_msg_lines.append("    %s" % nxtitem)
                    err_msg_lines.append("")
                else:
                    err_msg_lines.append("EXCLUDES: None")

                err_msg = os.linesep.join(err_msg_lines)
                self._logger.error(err_msg)

                result_code = -1

        return result_code


    def finalize(self): # pylint: disable=no-self-use
        """
            Called at the end of a test job in order to flush the results of the test run, copy
            the report template to the output directory.
        """
        return

    def query(self, format: CommandOutputFormat=CommandOutputFormat.DISPLAY):
        
        query_results = []

        with TestSequencer(self.title, self._testroot, includes=self.includes, excludes=self.excludes) as tseq:
            count = tseq.discover(test_module=self._test_module)

            query_results = tseq.references

            self._import_errors.extend(tseq.import_errors)

        return query_results

    @classmethod
    def user_interface_display_options(cls):
        """
            Overridden by derived TestJob classes in order to return a configuration user interface
            description that provides information about a vue javascript component that meets the
            interface requirements and will allow a user to display job configuration information that
            can be packaged stored in a data store as a json object and later passed to a job in order
            to configure the job.
        """
        return

    @classmethod
    def user_interface_edit_options(cls):
        """
            Overridden by derived TestJob classes in order to return a configuration user interface
            description that provides information about a vue javascript component that meets the
            interface requirements and will allow a user to input job configuration information that
            can be packaged stored in a data store as a json object and later passed to a job in order
            to configure the job.
        """
        return

    def _create_sequencer(self):
        """
            Simple hook function to make it possible to overload the type of the TestSequencer that is created
            for jobs.
        """
        inst = TestSequencer(self.title, self._testroot, includes=self.includes, excludes=self.excludes, metafilters=self.metafilters)
        return inst



class DefaultTestJob(TestJob):
    """
        The :class:`DefautTestJob` is utilized as a job container when a job was not specified.
    """
    name = "Test Job"
    description = "Unspecified test job."
