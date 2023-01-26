"""
.. module:: eventedvariablesink
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`EventedVariableSink` class which is used to act
               as a container for the evented variables for the instance of a class representing
               the state of a remote object that propagates evented variable values.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2022, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Any, Dict, Optional, Tuple, Union

import threading
import weakref

from datetime import datetime
from akit.exceptions import AKitNotOverloadedError

from akit.interop.eventsinking.eventedvariable import EventedVariable

class EventedVariableSink:
    """
        The :class:`EventedVariableSink` provides a mechanism for managing 
    """

    SINK_VARIABLE_TYPE = EventedVariable


    def __init__(self, variable_description_table: dict, state_lock: Optional[threading.RLock]=None, sink_prefix: str=None, auto_subscribe: bool=False):
        super().__init__()

        self._event_state_lock = state_lock
        if self._event_state_lock is None:
            self._event_state_lock = threading.RLock()

        self._sink_prefix = sink_prefix
        self._variable_description_table = variable_description_table

        self._auto_subscribe = auto_subscribe
        self._subscription_id = None
        self._subscription_expiration = None

        self._evented_variables: Dict[str, EventedVariable] = {}
        self._initiator_moment_register: Dict[str, Union[Tuple[datetime, Any], Tuple[None, None]]] = {}

        self._create_event_variables_from_list()

        return

    @property
    def auto_subscribe(self):
        return self._auto_subscribe

    @property
    def subscriptionId(self) -> str:
        """
            Returns the subscription ID of the current subscription.
        """
        return self._subscription_id

    @property
    def subscriptionExpiration(self) -> str:
        return self._subscription_expiration

    def initiator_moment_lookup(self, event_name: str) -> Union[Tuple[datetime, Any], Tuple[None, None]]:
        """
            Lookup the time of initiation for the event specified and any associated context information.

            :param event_name: The event identifier for the initiation moment being looked up.

            :returns: A tuple containing the last moment of initiation and context for the event specified.
        """

        rtnval = None, None

        for _ in self.yield_state_lock():
            if event_name in self._initiator_moment_register:
                rtnval = self._initiator_moment_register[event_name]

        return rtnval

    def initiator_moment_register(self, event_name: str, moment: datetime, context: Optional[Any]=None) -> None:
        """
            Registers the initiator time and context for a given initiator topic.

            :param event_name: The event identifier for the initiation moment being recorded.
            :param datetime: The datetime of the moment of initiation for a topic.
            :param context: Contextual information that provides more details around then initiation moment.
        """
        
        self._event_state_lock.acquire()
        try:
            self._initiator_moment_register[event_name] = (moment, context)
        finally:
            self._event_state_lock.release()

        return
    
    def lookup_event_variable(self, event_name: str) -> Union[EventedVariable, None]:
        """
            Looks up the specified event variable.

            :param event_name: The event name to find the :class:`EventedVariable` for.
        """
        varobj = None

        varkey = event_name
        if self._sink_prefix is not None:
            varkey = "{}/{}".format(self._sink_prefix, event_name)

        for _ in self.yield_state_lock():
            if varkey in self._evented_variables:
                varobj = self._evented_variables[varkey]

        return varobj

    def update_event_variable(self, event_name: str, event_value: Any, sink_locked: bool=False):

        varkey = event_name
        if self._sink_prefix is not None:
            varkey = "{}/{}".format(self._sink_prefix, event_name)

        if sink_locked:
            varobj = self._evented_variables[varkey]
            varobj.sync_update(event_value, expires=self._subscription_expiration, sink_locked=True)

        else:
            for _ in self.yield_state_lock():
                varobj = self._evented_variables[varkey]
                varobj.sync_update(event_value, expires=self._subscription_expiration, sink_locked=True)

        return

    def invalidate_subscription(self, scope: Optional[Any]=None):
        """
            Called in order to invalidate the subscription(s) specified by scope.

            :param scope: The scope of the subscriptions to renew.  If not specified then all
                          subscriptions should be renewed.
        """
        errmsg = "The `invalidate_subscription` method was not overloaded for type={}".format(type(self).__name__)
        raise AKitNotOverloadedError(errmsg)

    def renew_subscription(self, scope: Optional[Any]=None):
        """
            Called in order to renew the subscription(s) specified by scope. 

            :param scope: The scope of the subscriptions to renew.  If not specified then all
                          subscriptions should be renewed.
        """
        errmsg = "The `renew_subscription` method was not overloaded for type={}".format(type(self).__name__)
        raise AKitNotOverloadedError(errmsg)
    
    def trigger_auto_subscribe_from_variable(self, varkey: str):
        """
            Called in order to renew the subscription to the 

            :param varkey: The key for the variable that is triggering the auto-subscription process.
        """
        errmsg = "The `trigger_auto_subscribe_from_variable` method was not overloaded for type={}".format(type(self).__name__)
        raise AKitNotOverloadedError(errmsg)

    def yield_state_lock(self) -> threading.RLock:
        """
            Yields the state lock in a way that it can be automatically released at the end of an
            iteration scope.
        """
        self._event_state_lock.acquire()
        try:
            yield
        finally:
            self._event_state_lock.release()

    def _create_event_variable(self, event_name: str, **event_desc):
        """
            Creates an event variable and stores a reference to it in the variables table.

            :param event_name: The name of the event variable to create.
            :param data_type: The type of the event variable to create.
            :param default: The default value to set the new event variable to.
        """
        varkey = event_name
        if self._sink_prefix is not None:
            varkey = "{}/{}".format(self._sink_prefix, event_name)

        sink_ref = weakref.ref(self)
        event_var = self.SINK_VARIABLE_TYPE(varkey, event_name, sink_ref, **event_desc)
        self._evented_variables[varkey] = event_var

        return

    def _create_event_variables_from_list(self):
        """
            Called by the constructor to create the event variables listed from the variable descriptions
            detailed in the EVENTED_VARIABLE_DESCRIPTIONS table of the :class:`EventedVariableSink` derived type.
            We pre-create the event variables for each instance of an :class:`EventedVariableSink` type as the
            sink objects are designed to be used in a one to one, instance to remote object way.
        """

        for event_name in self._variable_description_table:
            event_desc = self._variable_description_table[event_name]
            self._create_event_variable(event_name, **event_desc)

        return
