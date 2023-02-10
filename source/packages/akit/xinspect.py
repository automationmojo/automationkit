"""
.. module:: xinspect
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains additional helper functions for inspecting python code and objects

.. note:: The modules that are named `xsomething` like this module are prefixed with an `x` character to
          indicate they extend the functionality of a base python module and the `x` is pre-pended to
          prevent module name collisions with python modules.

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


import inspect
import sys

def get_current_function_name():
    """
        Gets the function name of the current function which is calling get_current_function_name.
    """
    caller_func_name = None

    caller_stack = inspect.stack()[1]
    caller_func_name = caller_stack.frame.f_code.co_name

    return caller_func_name

def get_caller_function_name():
    """
        Gets the function name of the calling function which is the parent of the function calling
        get_caller_function_name or returns None if there is not stack frame available.
    """
    caller_func_name = None

    try:
        caller_stack = inspect.stack()[2]
        caller_func_name = caller_stack.frame.f_code.co_name
    except IndexError:
        pass

    return caller_func_name

def get_module_ancestry(module_name: str):

    module_list = []

    module_parts = module_name.split(".")
    module_parts_len = len(module_parts)

    for i in range(1, module_parts_len):
        ancestor_parts = module_parts[:i]
        amname = ".".join(ancestor_parts)

        amod = sys.modules[amname]
        module_list.append(amod)
    
    amod = sys.modules[module_name]
    module_list.append(amod)

    return module_list