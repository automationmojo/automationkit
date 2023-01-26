
from typing import Any, Optional, Tuple

import weakref

from datetime import datetime

from akit.interop.eventsinking.enumerations import EventedVariableState

class UpnpDefaultVar:
    """
        The UpnpDefaultVar object is utilized to handle the storage of the variables
        that the UpnpService has declared as fixed or not evented.
    """

    def __init__(self, key: str, name: str, service_ref: weakref.ref, value: Any = None, data_type: Optional[str] = None, default: Any = None,
                 allowed_list=None, timestamp: datetime = None, evented: bool = False):
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
        
        if evented:
            errmsg = "UpnpDefaultVar constructor was called for a variabled that is evented."
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
        return False

    @property
    def key(self) -> str:
        """
            The key {service type}/{event name} for this event.
        """
        return self._key

    @property
    def state(self) -> EventedVariableState:
        """
            The state of this event variable, UnInitialized, Valid or Stale
        """
        return EventedVariableState.Default

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

    def sync_read(self) -> Tuple[Any, datetime, datetime, EventedVariableState]:
        """
            Performs a threadsafe read of the value, updated, and state members of a
            :class:`UpnpEventVar` instance.
        """
        value, updated, changed, state = None, None, None, EventedVariableState.UnInitialized

        service = self._service_ref()
        for _ in service.yield_service_lock():
            updated = self._updated
            changed = self._changed

            state = EventedVariableState.Default

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
            for _ in service.yield_state_lock():
                orig_value = self._value
                self._value, self._updated = value, updated
                if orig_value != self._value:
                    self._changed = updated
                if expires is not None:
                    self._expires = expires

        return

    def __str__(self) -> str:
        value, updated, changed, state = self.sync_read()
        rtnstr = "name={} value={} updated={} changed={} state={}".format(self._name, value, updated, changed, state.name)
        return rtnstr