"""
.. module:: upnpeventvar
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`UpnpEventVar` class which is used to maintain
               variable subscription values and associated metadata.

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

from typing import Any, Tuple, Optional

import time
import weakref

from datetime import datetime, timedelta

from akit.exceptions import AKitTimeoutError
from akit.interop.upnp.services.upnpeventvarstate import UpnpEventVarState

EVENTVAR_WAIT_RETRY_INTERVAL = 1
EVENTVAR_WAIT_TIMEOUT = 60

class UpnpEventVar:
    """
        The UpnpEvent object is utilized to handle the storage and propagation
        of Upnp event values and updates and timeouts.

        NOTE: The properties associated with this object do not lock the
        subscription lock because they rely on eventual consistency.  They will
        always contain a value that was good at one point in time and will be
        updated in the future to a value that will be good for a new point in time.

        The "key" and "name" properties never change from thier initial values and
        they are set in the constructor when the object is under the control of only
        a single thread.

        If you need to ensure that the relationship between the value and updated
        members are in sync with each other, then a sync_read and sync_update
        API is provided to ensure this synchronization.
    """

    def __init__(self, key: str, name: str, service_ref: weakref.ref, value: Any = None, data_type: Optional[str] = None, default: Any = None,
                 allowed_list=None, timestamp: datetime = None, evented: bool = True):
        """
            Constructor for the :class:`UpnpEventVar` object.

            :param key: The key {service type}/{event name} for this event
            :param name: The name of the event this variable is storing information on.
            :param value: Optional initially reported value for the variable.  This is used when we have reports for
                          variables that we are not subscribed to.
            :param timestamp: The timestamp of the creation of this variable.  If a timestamp is passed then a value
                              needs to also be passed.
            :param evented: Indicates that this variable is evented to subscribers.
        """
        self._key = key
        self._name = name
        self._service_ref = service_ref
        self._value = value
        self._data_type = data_type
        self._default = default
        self._allowed_list = allowed_list
        self._timestamp = None
        
        if not evented:
            errmsg = "UpnpEventVar constructor was called for a variabled that is not evented."
            raise ValueError(errmsg)

        self._expires = None

        if self._value is not None and timestamp is None:
            self._timestamp  = datetime.now()

        if value is None and default is not None:
            self._value = default

        self._created = timestamp
        self._updated = timestamp
        self._changed = timestamp
        return

    @property
    def created(self) -> datetime:
        """
            When the event variabled value was set for the first time.
        """
        return self._created

    @property
    def changed(self) -> datetime:
        """
            A datetime object that indicates when the value was last changed in value.
        """
        return self._changed

    @property
    def expired(self) -> bool:
        """
            When the event variabled subscription has expired.
        """
        exp = False
        if self._expires is not None:
            now = datetime.now()
            if now > self._expires:
                exp = True
        return exp

    @property
    def key(self) -> str:
        """
            The key {service type}/{event name} for this event.
        """
        return self._key

    @property
    def state(self) -> UpnpEventVarState:
        """
            The state of this event variable, UnInitialized, Valid or Stale
        """
        rtn_state = UpnpEventVarState.UnInitialized

        updated = self._updated
        if updated == datetime.min:
            rtn_state = UpnpEventVarState.Stale
        elif updated is not None:
            rtn_state = UpnpEventVarState.Valid

        return rtn_state

    @property
    def updated(self) -> datetime:
        """
            A datetime object that indicates when the value was last updated.
        """
        return self._updated

    @property
    def name(self) -> str:
        """
            The name of the event this variable is storing information on.
        """
        return self._name

    @property
    def value(self) -> Any:
        """
            The last value reported for the event variable this instance is referencing.
        """
        return self._value

    def notify_byebye(self):
        """
            Handles a byebye notification and sets the updated property to
            None to indicate that this UpnpEventVar is stale and will not receive
            any further updates.

            NOTE: After the byebye has been received, the values of the variable
            can still be used but should be with the understanding that they are
            stale and should be used with caution.
        """
        self._expires = datetime.now()
        return

    def sync_read(self) -> Tuple[Any, datetime, datetime, UpnpEventVarState]:
        """
            Performs a threadsafe read of the value, updated, and state members of a
            :class:`UpnpEventVar` instance.
        """
        value, updated, changed, state = None, None, None, UpnpEventVarState.UnInitialized

        service = self._service_ref()
        for _ in service.yield_service_lock():
            updated = self._updated
            changed = self._changed

            if updated == datetime.min:
                state = UpnpEventVarState.Stale
            elif updated is not None:
                state = UpnpEventVarState.Valid

            value = self._value

        return value, updated, changed, state

    def sync_update(self, value: Any, expires: Optional[datetime] = None, service_locked: bool = False):
        """
            Peforms a threadsafe update of the value, updated and sid members of a
            :class:`UpnpEventVar` instance.
        """
        updated = datetime.now()

        if service_locked:
            orig_value = self._value
            self._value, self._updated = value, updated
            if orig_value != self._value:
                self._changed = updated
            if expires is not None:
                self._expires = expires
        else:
            service = self._service_ref()
            for _ in service.yield_service_lock():
                orig_value = self._value
                self._value, self._updated = value, updated
                if orig_value != self._value:
                    self._changed = updated
                if expires is not None:
                    self._expires = expires

        return

    def wait_for_update(self, moment: datetime, timeout: float = EVENTVAR_WAIT_TIMEOUT, interval: float = EVENTVAR_WAIT_RETRY_INTERVAL) -> Any:
        """
            Takes a datetime timestamp that is taken before a modification is made that
            will cause a state variable update and waits for the updated timestamp of
            this :class:`UpnpEventVar` instance to set to a timestamp that comes after the
            pre modification timestamp.

            :param moment: A timestamp taken from datetime.now() at a moment prior to engaging in
                            an activity that will result in a state variable change.
            :param timeout: The time in seconds to wait for the update to occur.
            :param interval: The time interval in seconds to wait before attempting to retry and
                             check to see if the updated timestamp has changed.

        """
        if self.expired:
            # If wait_for_update is being called, that means the caller wants a fresh
            # copy of the value for this event.  If this event is not evented, then
            # try renewing the service subscription to see if we are given a value for
            # this variable when we renew our subscription.
            service = self._service_ref()
            service.renew_subscription()

        now_time = datetime.now()
        start_time = now_time
        end_time = start_time + timedelta(seconds=timeout)
        while True:
            if now_time > end_time:
                raise AKitTimeoutError("Timeout waiting for event variable to update.") from None

            if self._updated is not None and self._updated > moment:
                break

            time.sleep(interval)
            now_time = datetime.now()

        return self._value

    def wait_for_value(self, timeout: float = EVENTVAR_WAIT_TIMEOUT, interval: float = EVENTVAR_WAIT_RETRY_INTERVAL) -> Any:
        """
            Waits for this :class:`UpnpEventVar` instance to contain a value.  It constains a
            value once the updated timestamp has been set.

            :param timeout: The time in seconds to wait for a value to be present.
            :param interval: The time interval in seconds to wait before attempting to retry and
                             check to see if the updated timestamp has been set.
        """
        now_time = datetime.now()
        start_time = now_time
        end_time = start_time + timedelta(seconds=timeout)
        while True:
            if now_time > end_time:
                raise AKitTimeoutError("Timeout waiting for event variable to update.") from None

            if self._updated is not None:
                break
            time.sleep(interval)
            now_time = datetime.now()

        return self._value

    def __str__(self) -> str:
        value, updated, changed, state = self.sync_read()
        rtnstr = "name={} value={} updated={} changed={} state={}".format(self._name, value, updated, changed, state.name)
        return rtnstr
