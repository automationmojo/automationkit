from typing import Optional
from types import ModuleType

def parse_test_include_expression(expression: str, testmodule: Optional[ModuleType], method_prefix: str = "test"):
    """
        Parses the test include expression in connection with the testmodule and method_prefix information provided
        and returns the components (package, module, testclass, testname) which can be used to perform a
        test tree search for included tests based on the expression.

        :param expression: A test include expression in the form of (package).(module)@(testclass)#(testcase).  The module,
                           testclass, and testcase are optional.  If these items are excluded every descendant test found
                           under the (package) will be included.
        :param testmodule: A test module that contains the tests to be run.  This is passed when a individual test file
                           debugging workflow is being used.
        :param method_prefix: The string prefix that identifies test methods on a :class:`TestContainer` derived class.
    """

    expr_package = None
    expr_module = None
    expr_testclass = None
    expr_testname = None

    # If test_module was passed then we are running a test module as a script or debugging a test module
    # so we handle the special case where we only collect the test references from the test module that
    # was set.
    if testmodule is not None:
        if expression.find(".") > -1 or expression.find("@") > -1 or expression.find(":") > -1:
            raise ValueError("parse_test_include_expression: The include expression for test module runs should only have a " \
                             "test class and test method.")

        testmodule_name = testmodule.__name__

        expr_package = "*"
        expr_module = "*"

        # If the full path to the module was set correctly by the generic entry point, then replace the package and module
        # expressions with exact expressions so we don't load coad that does not need to be loaded when we are scanning
        # for tests.
        if testmodule_name != "__main__":
            tm_name_parts = testmodule_name.split('.')
            if len(tm_name_parts) > 1:
                expr_package = '.'.join(tm_name_parts[:-1])
                expr_module = tm_name_parts[-1]

        if expression.find("#") > -1:
            expression, expr_testname = expression.split("#")
            if not expr_testname.startswith(method_prefix):
                raise ValueError("parse_test_include_expression: The testname component of the expression must start with the " \
                                "method_prefix=%r. expression%r" % (method_prefix, expression))

        if expression == "*":
            expr_testclass = None

    # If self._test_module was not set then we are performing a commmandline run where a test job or includes, excludes
    # collection was passed we need to use one of those to determine what to run.
    else:
        # Start from the end of the expression and work backwards to determine what components in the expression were passed

        # First look for the # to see if we have a test name specified.
        if expression.find("#") > -1:
            expression, expr_testname = expression.split("#")
            if not expr_testname.startswith(method_prefix):
                raise ValueError("parse_test_include_expression: The testname component of the expression must " \
                                "start with the method_prefix=%r. expression%r" % (method_prefix, expression))

        if expression.find("@") > -1:
            expression, expr_testclass = expression.split("@")

        if expr_testclass == "":
            expr_testclass = None

        comb_expr_comp = expression.split(".")
        if len(comb_expr_comp) > 1:
            expr_package = ".".join(comb_expr_comp[:-1])
            expr_module = comb_expr_comp[-1]
        else:
            expr_package = None
            expr_module = expression

    return expr_package, expr_module, expr_testclass, expr_testname
