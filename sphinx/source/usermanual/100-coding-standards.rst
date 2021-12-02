****************
Coding Standards
****************

**in-progress**

Sections
========
  * `Class Variable Initialization`_
  * `Code Optimization`_
  * `Multiline Error Message Formation`_
  * `Return Statements`_

Class Variable Initialization
=============================
All variables must be initialized the constructor of the class.

.. code-block:: python

    class Blah:
        def __init__(self):
            self._a = 0
            self._b = 0
            self._c = ""
        
        def set_to_blah(self):
            self._c = "blahblah"

This is very important for visual debuggers and tools to perform type
inferencing and popup context typing help.  The tools will inspect the
constructor to see what variables are attached to **self**.  It also ensures
that an initial value is present any time a variable is used.  The following is
**NOT** allowed:

.. code-block:: python

    class Blah:
        def __init__(self):
            self._a = 0
            self._b = 0
        
        def set_to_blah(self):
            self._c = "blahblah"

Code Optimization
=================

The desired characteristics of test code is different than that of production
code.  Test code is often used to debug or step through scenarios and workflows
in order to capture information about what is going on in the code that is the
target of the tests.  Because test code is used so often in the debugger to
perform investigations of product bugs and test issues, test code should only
be optimized where there is sufficient data to show that a specific are of code
is having a big negative impact on the performance of the test runs.

The reality of distributed automation frameworks is that they spend alot of
time in interop APIs looping on retry attempts with delays intentionally
inserted between retries.  Code that is intentionally being delayed should
**NOT** be the target of code optimizations.  The following is a list of
optimization techniques that are discouraged in the test code so the test code
can exhibit more of the desired characteristics list above.

* One Liners or Excessive Brevity
* Nested Inlining Function Calls
* Compound return statements

I cannot stress enough that if poor test coding styles are used too much in a
large code base and if the practice goes on for too long.  The code will be
difficult to work in and the productivity of the consumers of the test code
will be greatly impacted.

One Liners and Brevity Shortcuts
--------------------------------

One liners and code written with the intent of being brief are not allowed and
or discourage in the automation code.  This is because ensuring the automation
code can be easily run and stepped through in the debugger is a primary requirment.
Simple list comprehensions that get assigned to a local variable are ok such as:

.. code-block:: python

    dev_list = [ dev for dev in device_list ]


These are acceptable because you can easily see the result of the list comprehension
in the debugger after the comprehension has run.  However, if the list comprehension
becomes more complexed with if statements calling functions, then you should
break out the list creation into mutliple lines like so:

.. code-block:: python

    dev_list = []
    for dev in device_list:
        if dev.deviceType == 'network/upnp':
            dev_list.append(dev)


This is most likely a little less performant. Squeezing every last bit of performance
out of the code is **NOT** a priority of creating test code that is easy to
consume, maintainable and easy to debug.

Nested Inlining Function Calls
------------------------------

An important aspect of code that is friendly to debug is that it spreads out
statements across multiple lines of code.  By spreading out code statement such
as function calls or index accesses across mutliple lines, we attach metadata in
the form of a line number to the statements which enables the debugger to work
more efficiently with the statements.

The following code is not debugger friendly or efficient because the statements
do not have unique line numbers associated with them in the python byte code.

.. code-block:: python

    some_function(param_function_a(), param_function_b(), param_function_c())

Another thing to keep in mind is that indexers in python are actually function calls
so statements like the ones below are also undesired in test code.

.. code-block:: python

    some_function(data[0], data[1], data[2])

A better way to get data items from a squence or list would be to expand the sequence
to variables We like so:

.. code-block:: python

    a, b, c = data
    some_function(a, b, c)

Compound Return Statements
--------------------------

.. code-block:: python

    def some_function():
        return inner_function_call(inner_a(), inner_b(), inner_c(), inner_d())

For more details about how returns should be written, see the `Return Statements`_ section.

Multiline Error Message Formation
=================================

An important part of creating greate automation frameworks and tools is the sharing of
expert knowledge between consumers of the automation framework code base.  A great way
to implement knowledge sharing is to write code so that it provides detailed contextual
information when errors occur.  This is important because the last person working or dealing
with an issue in the error handling code is working on the problem and has the best
knowledge about the context when the error occurs and should share that knowledge with others.

As part of providing well formed and detailed error reporting, we want to be able to see
and debug the code that is creating the error messages.  When creating multi-line error
messages, the following method is preferred.

* Create a list to hold the error message lines
* Iterate any data collections or collect data and append lines to the list
* Create section headers for individual data sections
* Join the list of error message lines together using os.linesep.join() and assign the
  message to a variable so it can be seen in the debugger
* pass the error message variable to the exception

The code below provides an example of the building of a detailed error message that is easy to debug.

.. code-block:: python

    err_msg_lines = [
        "Failed to find expected UPNP devices after a timeout of {} seconds.".format(response_timeout)
    ]
    err_msg_lines.append("EXPECTED: ({})".format( len(expected_devices) ))
    for dkey in expected_devices:
        err_msg_lines.append("    {}:".format(dkey))
    err_msg_lines.append("")
    
    err_msg_lines.append("MATCHING: ({})".format( len(scan_context.matching_devices) ))
    for dkey in scan_context.matching_devices:
        err_msg_lines.append("    {}:".format(dkey))
    err_msg_lines.append("")
    
    err_msg_lines.append("FOUND: ({})".format( len(scan_context.found_devices) ))
    for dkey in scan_context.found_devices:
        err_msg_lines.append("    {}:".format(dkey))
    err_msg_lines.append("")
    
    err_msg_lines.append("MISSING: ({})".format( len(missing) ))
    for dkey in missing:
        err_msg_lines.append("    {}:".format(dkey))
    err_msg_lines.append("")
    
    err_msg = os.linesep.join(err_msg_lines)
    raise AKitTimeoutError(err_msg) from None


Return Statements
=================

All functions or methods that are not generators should have a `return` statement.  The return
statements are important for three reasons:

* It prevents the formation of appended functionality during a bad code merge
* It provides line number data for the debugger
* It provides a way to check results, in context, before a return
* It make code easier to read

Below is a detailed description of each of these issues.

Formation of Appended Functionality
-----------------------------------

One of the common tasks that is performed frequently by software developer is the refactoring or
merging of code.  During the process of refactoring or merging code, function declarations might
be missed or incorrectly deleted.  When this happens, new functionality can end up being inadvertantly
appended to the previous function in the code.  Take the following two functions as a simplified example.

.. code-block:: python

    def say_hello():
        print("Hello")
    
    def say_world():
        print("World")


If returns are not present at the end of the functions above, during a refactor or code merge it
is possible for lines of code to be removed, like if the `say_world` function declaration was
deleted like so:

.. code-block:: python

    def say_hello():
        print("Hello")
    
        print("World")


Now, without warning from python, the functionality of the `say_world` function has been appended
to the `say_hello` function and thus changes the functionality of the `say_hello` function without
warning.

Now lets look at what would happen if the same thing took place when return statements are utilized
as in the code below.

.. code-block:: python

    def say_hello():
        print("Hello")
        return
    
    def say_world():
        print("World")
        return

In the code above, we clearly mark the end of our functions so python has a better chance of doing
the correct thing when code is modified incorrectly.  If the function declaration for `say_world`
is removed like so.

.. code-block:: python

    def say_hello():
        print("Hello")
        return

        print("World")
        return


In the case above, python will not execute the stagling code and will not append its functionality
to the `say_hello` method.  Also, the python linter can show the remaining code body for `say_world`
as dead code or unreachable code and complain when it tries to lint the code in the file.

Line Number for Debugging
-------------------------
A very important aspect of test code is debuggability.  In order to be able to inspect the results
of a function before it returns, you need a line of code to hang a breakpoint on. By stopping the
debugger on the return statement, you can see the values of the inputs to the function and values
of any intermediate byproducts or local variables in the context of the function.

.. code-block:: python

    import dis
    
    def function_with_return(a: int, b: int):
        if a + b == 99:
            print ("Hello '99'")
        return
    
    def function_without_return(a: int, b: int):
        if a + b == 99:
            print ("Hello '99'")
    
    print("==== FUNCTION WITH RETURN ====")
    fwr_assem = dis.dis(function_with_return)
    print(fwr_assem)
    print("")
    
    
    print("==== FUNCTION WITHOUT RETURN ====")
    fwor_assem = dis.dis(function_without_return)
    print(fwor_assem)
    print("")


.. code-block:: text

    ==== FUNCTION WITH RETURN ====
    4           0 LOAD_FAST                0 (a)
                2 LOAD_FAST                1 (b)
                4 BINARY_ADD
                6 LOAD_CONST               1 (99)
                8 COMPARE_OP               2 (==)
                10 POP_JUMP_IF_FALSE       20
    
    5          12 LOAD_GLOBAL              0 (print)
                14 LOAD_CONST               2 ("Hello '99'")
                16 CALL_FUNCTION            1
                18 POP_TOP
    
    6     >>   20 LOAD_CONST               0 (None)  # Has a Distict Line Number (6)
                22 RETURN_VALUE
    None


Distinct lines of code, which have an associated line number, are very important for enabling a
great debugging experience.  Without a distinct line of code or line number, there is no place
to hang a breakpoint on a piece of code that is associated with the bytecode of a program.

.. code-block:: text

    ==== FUNCTION WITHOUT RETURN ====
    9           0 LOAD_FAST                0 (a)
                2 LOAD_FAST                1 (b)
                4 BINARY_ADD
                6 LOAD_CONST               1 (99)
                8 COMPARE_OP               2 (==)
                10 POP_JUMP_IF_FALSE       20

    10          12 LOAD_GLOBAL              0 (print)
                14 LOAD_CONST               2 ("Hello '99'")
                16 CALL_FUNCTION            1
                18 POP_TOP
            >>   20 LOAD_CONST               0 (None)  # Has NO Line Number
                22 RETURN_VALUE
    None


In Context Return Verification
------------------------------

One of the most important aspects of writing debuggable code, is to write code in such a way that
you can see the values of the local variables that contributed to the creation of the value being
returned.  The following is an example function that demonstrates the concept of writing functions
so the context of the return value can be examined.

.. code-block:: python

    def example_function(a: int, b: int) -> int:

        multiplier = random.randint(0, 10)

        rtnval: int = (a + b) * multiplier
        
        return rtnval


From looking at the simple example above, you can see that in order to debug the function and
make sure it is returning the correct answer, it is useful to be able to see the `multiplier`
parameter that is generated locally and is being used to effect the output.  Providing a simple
independant return allows us to see the context that is generating the output value.  Another
example below shows how a function like this might be written that will not provide the same
ability to debug the function.

.. code-block:: python

    def example_function(a: int, b: int) -> int:
        return (a + b) * random.randint(0, 10)


This function is sometimes valued by some developers for its brevity, but for testing purposes
this coding style results in reduced quality code. The reason the code is reduced quality is
because you cannot see the context of the return value being generated.  If you put a breakpoint
on the `return` statement, you don't see the resulting value until you step out into the calling
function context. When you step out of the function to its calling function to see the return value,
the local variables of the `example_function` and the context that generated the return value is
no longer available. Upon the return of the function, the stack was popped and the context went away.

Because of the importance of examining the context that generates a returned value, it is always
prefered to create a local variable in order to effect a simple return like so:

.. code-block:: python

    def example_function(a: int, b: int, c: int):
        rtnval = (a + b) * c
        return rtnval


Vise a complexed return statement such as

.. code-block:: python

    def example_function(a: int, b: int, c: int):
        return (a + b) * c


Code Legibility
---------------

Finally, `return` statements are important to improve the legibility of code. Because python code
uses indentation to determine scope, the repeated indentation of successive code blocks can present
issues with the readability of code. This can particularly be a problem with longer functions.  The
example code below demonstates the improvement of ligibility that a return statement can offer.

.. code-block:: python

    def example_function(a: Optional[int], b: Optional[int], c: Optional[int], d: Optional[int]):
        val = None

        if a is not None:
            print (a)
            if b is not None:
                print (a + b)
                if c is not None:
                    print ((a + b) * c)
                    if d is not None:
                        print ((a + b) * c) + d
        return

For the code above, it is clear where the end of the function resides as it has a return.  This can
be particularly important if this was a longer function.

For the function below, it might be a little more confusing where a function ends in a larger block
of code.

.. code-block:: python

    def example_function(a: Optional[int], b: Optional[int], c: Optional[int], d: Optional[int]):
        rtnval = None
    
        if a is not None:
            print (a)
            if b is not None:
                print (a + b)
                if c is not None:
                    print ((a + b) * c)
                    if d is not None:
                        print ((a + b) * c) + d


For consistency and to help resolve all of these issues, I prefer to use returns on all of my functions
and methods.  Any function or method that is not a generator, since generators don't have returns.