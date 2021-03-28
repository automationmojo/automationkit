"""
.. module:: tasklink
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`TaskLink` class used to create chains of tasks.

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

from typing import Any

class TaskLink:
    """
        The :class:`TaskLink` object provides a mechanism for creating chains of executable
        tasks that are executed as a chain which are walked to setup and execute tasks and then
        back-walked in order to process and respond to results.

        A :class:`TaskLink` can function as link in a longer execution chain in which case it will
        have properties that provide access to types of links that can be added to extend the execution
        chain.

        A :class:`TaskLink` can also function as a terminal link in an execution chain in which case it
        will provide an action method of some sort that will trigger the execution of the chain execution
        build up or setup, execute a task, and then propogate a result back down the execution chain.
    """

    def __init__(self, parent, chain, name):
        self._parent = parent
        self._chain = chain
        self._name = name
        self._args = None
        self._kwargs = None
        return

    def __call__(self, **kwargs):
        """
            Called when a link instance is being called with the parameters that are
            being provided setup the execution of the link and to set the chain execution
            context of the link.
        """
        self.set_params(**kwargs)
        self._chain.append(self)
        return self

    def walk(self):
        """
            Method called to activate the walking of the task chain.
        """
        walker = self._walker()

        base = next(walker)
        results = base.execute(walker)

        return results

    def execute(self, walker) -> Any:
        """
            Overloaded by derived types as a executiion method in a call chain that will
            setup a call condition and then call to the next member in the execution chain.

            :param walker: An interator that is used to walk down the task chain.  The walker
                           is iterated with next to get the next link in the chain.
        """
        this_type = type(self)
        type_name = this_type.__name__

        # Setup
        print("{}: Setting Up".format(type_name))

        # Do work and get result
        nextlink = next(walker)
        result = nextlink.execute()

        # Teardown
        print("{}: Tearing Down".format(type_name))

        return result

    def set_params(self, **kwargs):
        """
            Overloaded by derived TaskLink types in order to accept parameters and save them
            to internal instance variables.
        """
        self._kwargs = kwargs
        return

    def _walker(self):
        """
            Iterator for walking the task chain.
        """
        chain = [link for link in self._chain]

        for link in chain:
            yield link

    def __repr__(self):
        """
            Creates a string representation of this link and its parent links.
        """
        strrepr = ""

        if self._parent is not None:
            strrepr = "%s." % repr(self._parent)

        kwarg_str = ""
        for kname, kval in self._kwargs:
            kwarg_str += "%s=%r," % (kname, kval)
        kwarg_str.rstrip(",")

        strrepr += "%s(%s)" % (self._name, kwarg_str)

        return strrepr

    def __str__(self):
        """
            Creates a string decription of the link and its parent connected links.
        """
        return repr(self)

