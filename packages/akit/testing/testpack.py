"""
.. module:: akit.testing.testpack
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is contains the :class:`TestPack` class which is utilized as the collection point
               which associates a set of tests with their execution scopes.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

class TestPack:
    """
              --------------
              |  TestPack  |
        -------------------------
        |  Scope A  |  Scope B  |
        -------------------------     
        |         Scope C       |     
        -------------------------     

        Pack:
            * Single instance
            * Collect or Group tests
            * Associates scopes of execution with the tests
            * Allows for the customization of the Setup and TearDown of scopes
        
        Scopes:
            * Collect Resources utilized in a Scope of Execution for a group of tests
            * Setup and TearDown of scope

    """

    name = ""           # TestPack Friendly Name
    description = ""    # TestPack Description
    
    # Includes and excludes can be added to a TestPack in order to help the test framework reduce
    # the amount of resources that need to be expended in order to scan for the tests that are linked
    # to a TestPack
    searchin = None

    context = None # The scopes associated with a testpack, scopes

    def acclimate(self, testlandscape):
        """
            API called by the test framework in order to acclimate the :class:`TestPack` to the :class:`.
            When this method is called on a :class:`TestPack` it can analyze the testlandscape and configure
            internal state that can be used to determine which tests are applicable to the given test
            landscape.
        """
        return 

    def expectations(self):
        """
            Method that can be implemented by derived classes or updated dynamically to reflect the
            expected torun and skipped test counts for a given testlandscape.  The test framework will call the 'acclimate'
            method prior to calling this method in order to let the 'TestPack' analyze the testlandscape
            and determine which tests are applicable to the test 

            (torun, skipped)
        """
        return

    def run(self, presult):
        """
            Runs the tests associated with this :class:`TestPack` as a child result container of the parent
            result container that was passed to this method.

            :param presult: The parent result container to append test runs results to as child results.
            :type presult: :class:`akit.results.ResultContainer`

        """

        setup_success = False
        try:
            setup_success = self.enter_scopes()
        except:
            pass

        if setup_success:
            pass
        else:
            # Mark all the tests as error
            pass

        try:
            self.exit_scopes()
        except:
            pass

        return

    def traverse_package(self, recorder, parent_inst=None):

        pack_key = self.__module__ + "." + self.__name__
        logger.info("TESTPACK ENTER: %s" % pack_key)

        try:
            res_inst = str(uuid.uuid4())

            result_container = ResultContainer(res_inst, pack_key, ResultType.PACKAGE, parent_inst=parent_inst)
            recorder.record(result_container)

            self.scopes_enter(scope)

            if scope_key in ScopeMixIn.test_references:
                test_references = ScopeMixIn.test_references[scope_key]
                for tref in test_references:

                    try:
                        # Create an instance of the test case using the test reference
                        testinst = tref.create_instance(leaf_scope, recorder)

                        # Run the test, it shouldn't raise any exceptions unless a stop
                        # is raised or a framework exception occurs
                        testinst.run(result_container.result_inst)
                    except Exception as xcpt:
                        pass

        finally:
            try:
                self.scopes_exit(scope)
            except Exception as xcpt:
                #TODO: Handing exception logging here
                pass

            logger.info("SCOPE EXIT: %s" % scope_key)

        return

    def scopes_enter(self):
        """
        """

        rev_mro = list(self.__mro__)
        rev_mro.reverse()

        for nxt_cls in rev_mro:
            if is_scope_mixin(nxt_cls):
                nxt_cls.scope_enter()
                if not hasattr(nxt_cls, "scope_enter_count"):
                    nxt_cls.scope_enter_count = 1
                else:
                    nxt_cls.scope_enter_count += 1

        return

    def scopes_exit(self):
        """
        """

        norm_mro = list(self.__mro__)

        for nxt_cls in norm_mro:
            if is_scope_mixin(nxt_cls):
                nxt_cls.scope_exit()
                if hasattr(nxt_cls, "refcount"):
                    nxt_cls.refcount -= 1
                else:
                    logger.error("ERROR: Every scope should have a 'refcount' class variable.")

        return


