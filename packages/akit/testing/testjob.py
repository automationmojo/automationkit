"""
.. module:: akit.testing.testjob
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

import os
import uuid

from akit.environment.context import ContextUser

from akit.integration.landscaping import Landscape
from akit.recorders import JsonResultRecorder
from akit.results import ResultContainer, ResultType
from akit.testing.testsequencer import TestSequencer

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

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
            Creates an instance of a TestJob and then returns that instance of the TestJob for all subsequent
            calls to create test Job instances.
        """
        if cls._instance is None:
            cls._instance = super(TestJob, cls).__new__(cls)
        return cls._instance

    def __init__(self, logger, testroot, includes=None, excludes=None, test_module=None, parser=None,
                 branch=None, build=None, flavor=None):
        """
            Constructor for a :class:`TestJob`.  It initializes the member variables based on the parameters passed
            from the entry point function and the class member data declared on :class:`TestJob` derived classes.
        """
        self._logger = logger
        self._testroot = testroot

        if self.includes is None:
            self.includes = includes
            self.excludes = excludes

        self._test_module = test_module
        self._parser = parser
        self._starttime = None

        self._test_results_dir = None
        self._result_filename = None
        self._summary_filename = None
        self._import_errors_filename = None

        self._testpacks = None
        self._branch = branch
        self._build = build
        self._flavor = flavor
        return

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, ex_type, ex_inst, ex_tb):
        self.finalize()
        return False

    def begin(self):
        """
            Called at the beginning of a test job in order to setup the recording of test results.
        """

        env = self.context.lookup("/environment")

        self._test_results_dir = env["output_directory"]
        self._starttime = env["starttime"]

        self._result_filename = os.path.join(self._test_results_dir, "testrun_results.jsos")
        self._summary_filename = os.path.join(self._test_results_dir, "testrun_summary.json")
        self._import_errors_filename = os.path.join(self._test_results_dir, "import_errors.jsos")

        return

    def execute(self):
        """
            Runs the tests that are included in the given :class:'TestPack'.
        """
        result_code = 0

        with TestSequencer(self.title, self._testroot, includes=self.includes, excludes=self.excludes) as tseq:
            # IMPORTANT: The ordering of the automation sequence is extremely important.  Proper
            # ordering of these steps ensures that the correct things are happening in the correct
            # order in the automation code and that we provide the ability for configuration
            # issues to be discovered as early as possible.

            # STEP 1: We discover the tests first so we can build a listing of the
            # Integration and Scope mixins.  We don't want to execute any test code, setup,
            # or teardown code at this point.  We want to seperate out the integration
            # code from the test code and run the integration code first so we can discover
            # integration issues independant of the test code itself.
            count = tseq.discover(test_module=self._test_module)

            # STEP 2: Tell the sequencer to record any import errors that happened during discovery
            # of tests.  If a test file or dependent file failed to import then the test
            # will just not be included in a run and this is a type of invisible error
            # that we must plan for and highlight.
            tseq.record_import_errors(self._import_errors_filename)

            if count > 0:

                # STEP 3: If there are tests that were discovered. Provide an opportunity for any Integration
                # or Scope mixins associated with the descovered tests to publish the intergation points they
                # use to engage with the framework and environment.
                tseq.publish_integrations()

                # STEP 4: Parse the extended arguments, the publish phase would have allowed
                # the mixins to register extended arguments, so now parse those arguments to ensure
                # that any extended arguments that are needed by the included tests were actually
                # provided.  This provides for a dynamic and rich arguement processing mechanism
                # that can vary based on the tests that were included in the run.
                if self._parser is not None:
                    # Parse any extended arguments now that were published by the integrations
                    tseq.parse_extended_args(self._parser)

                # Initiate contact with the TestLandscape
                landscape = Landscape()

                # STEP 5: Now that we have collected all the mixins and have a preview of
                # the complexity of the automation run encoded into the mixin types collected.
                # Allow the mixins to attach to the automation environment so they can get
                # a preview of the parameters and configuration and provide us with an early
                # indicator of any parameter or configuration issues.
                #
                # This is the final step of validating all the input information to the run and
                # we are able to perform this step in the context of the integration code and 
                # outside of the execution of any test code
                tseq.attach_to_environment() 

                # STEP 6: All the mixins have had a chance to analyze the configuration
                # information and provide us with a clear indication if there are any configuration
                # issues.  Now provide the mixins with the opportunity to reach out to the
                # automation infrastructure and checkout or collect any global shared resources
                # that might be required for this automation run.
                tseq.collect_resources()

                # STEP 7: Because the Automation Kit is a distrubuted automation test framework,
                # we want to provide an early opportunity for all the integration and scope mixins
                # to establish initial connectivity or first contact with the resources or devices
                # that are being integrated into the automation run.
                #
                # This helps to ensure the reduction of automation failure noise due to configuration
                # or environmental issues
                tseq.establish_connectivity()

                title = self.title
                runid = str(uuid.uuid4())
                start = str(self._starttime)
                sum_file = self._summary_filename
                res_file = self._result_filename
                branch = self._branch
                build = self._build
                flavor = self._flavor

                # STEP 8: The startup phase is over, up to this point we have mostly been executing
                # integration code and configuration analysis code that is embedded into mostly class
                # level methods.
                #
                # Now we start going through all the test testpacks and tests and start instantiating
                # test scopes and instances and start executing setup, teardown and test level code
                with JsonResultRecorder(title, runid, start, sum_file, res_file, branch=branch, build=build, flavor=flavor) as recorder:
                    # Traverse the execution graph
                    self._testpacks = tseq.testpacks
                    result_code = tseq.execute_testpacks(runid, recorder, self.sequence)

                # STEP 9: This is where we do any final processing and or publishing of results.
                # We might also want to add automated bug filing here later.

            else:
                # We didn't find any tests so display a message, and set the return code to
                # indicate an error condition
                err_msg = "The include and exclude parameters specified resulted in an empty test set."
                if self.includes is not None:
                    err_msg += "INCLUDES:\n    %s\n" % "    \n".join(self.includes)
                else:
                    err_msg += "INCLUDES: None\n"
                if self.excludes is not None:
                    err_msg += "EXCLUDES:\n    %s\n" % "    \n".join(self.excludes)
                else:
                    err_msg += "EXCLUDES: None\n"
                self._logger.error(err_msg)
                result_code = -1

        return result_code


    def finalize(self):
        """
            Called at the end of a test job in order to flush the results of the test run, copy
            the report template to the output directory.
        """
        return

    def sequence(self):
        """
            Overridden by derived TestJob classes in order to customize the sequence of execution for the
            'TestPack'(s) associated with the TestJob.
        """
        for tp in self._testpacks:
            yield tp

    @classmethod
    def user_interface_display_options(cls):
        """
            Overridden by derived TestJob classes in order to return a configuration user interface
            description that provides information about a vue javascript component that meets the
            interface requirements and will allow a user to input job configuration information that
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

class DefaultTestJob(TestJob):
    name = "Test Job"
    description = "Unspecified test job."

    def __init__(self, context, logger, testroot, includes=None, excludes=None, test_module=None):
        super(DefaultTestJob, self).__init__(context, logger, testroot, includes=includes, excludes=excludes, test_module=test_module)
        return
