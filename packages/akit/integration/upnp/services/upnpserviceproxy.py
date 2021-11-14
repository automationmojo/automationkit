"""
.. module:: upnpserviceproxy
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`UpnpServiceProxy` class which is the base class
               all services proxied.

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

from typing import Optional, Union

import os
import threading
import time
import traceback
import weakref

from datetime import datetime, timedelta

import requests

from akit.aspects import Aspects, ActionPattern, DEFAULT_ASPECTS

from akit.environment.context import Context

from akit.xlogging.foundations import getAutomatonKitLogger
from akit.xlogging.scopemonitoring import MonitoredScope

from akit.exceptions import AKitRuntimeError, AKitTimeoutError

from akit.integration.upnp.soap import SoapProcessor, SOAP_TIMEOUT
from akit.integration.upnp.upnpconstants import DEFAULT_UPNP_CALL_ASPECTS
from akit.integration.upnp.upnperrors import UpnpError
from akit.integration.upnp.services.upnpdefaultvar import UpnpDefaultVar
from akit.integration.upnp.services.upnpeventvar import UpnpEventVar
from akit.integration.upnp.xml.upnpdevice1 import UpnpDevice1Service

logger = getAutomatonKitLogger()

LITERAL_UPNPDEVICE_TYPE = 'akit.integration.upnp.devices.upnpdevice.UpnpDevice'

class UpnpServiceProxy:
    """
        The :class:`UpnpServiceProxy` object provides that base data and functional methods for providing
        inter-operability with a devices Service.  It provides methods for making calls on actions and
        access to methods for making subscriptions.
    """

    SERVICE_ID = None
    SERVICE_TYPE = None

    SERVICE_DEFAULT_VARIABLES = {}

    SERVICE_EVENT_VARIABLES = {}

    def __init__(self):
        self._device_ref = None
        self._soap_processor = SoapProcessor()

        self._host = None
        self._baseURL = None

        self._controlURL = None
        self._eventSubURL = None
        self._SCPDURL = None
        self._serviceType = None

        self._serviceId = None

        self._validate_parameter_values = True

        self._service_lock = threading.RLock()
        self._subscription_id = None
        self._subscription_expiration = None

        self._default_variables = {}
        self._evented_variables = {}
        self._create_default_variables_from_list()
        self._create_event_variables_from_list()

        self._logged_events = None
        if self.SERVICE_TYPE is not None:
            ctx = Context()
            logged_events_by_service = ctx.lookup("/environment/configuration/networking/upnp/subscriptions/logged-events")
            if logged_events_by_service is not None and self.SERVICE_TYPE in logged_events_by_service:
                self._logged_events = logged_events_by_service[self.SERVICE_TYPE]
        return

    @property
    def baseUrl(self) -> str:
        """
            Returns the base URL for working with a service.
        """
        return self._baseURL

    @property
    def controlURL(self) -> str:
        """
            Returns the control URL that is used making calls on actions on a device service.
        """
        return self._controlURL

    @property
    def device(self) -> LITERAL_UPNPDEVICE_TYPE:
        """
            Returns a reference to the parent device of this service.
        """
        return self._device_ref()

    @property
    def eventSubURL(self) -> str:
        """
            Returns the URL that is used to subscribe to events.
        """
        return self._eventSubURL

    @property
    def host(self) -> str:
        """
            The host associated with the parent device.
        """
        return self._host

    @property
    def SCPDURL(self) -> str:
        """
            The URL called to retrieve the service description document.
        """
        return self._SCPDURL

    @property
    def serviceId(self) -> str:
        """
            Returns the service ID
        """
        return self._serviceId

    @property
    def serviceType(self) -> str:
        """
            Returns the service Type ID.
        """
        return self._serviceType

    @property
    def subscriptionId(self) -> str:
        """
            Returns the subscription ID of the current subscription.
        """

    def call_action(self, action_name: str, arguments: dict = {}, auth: dict = None, headers: dict = {}, aspects: Aspects=DEFAULT_UPNP_CALL_ASPECTS):
        """
            Method utilize to make direct calls on a service for action APIs that are not published in a service description.

            :param action_name: The action name to make a call on.
            :param arguments: The arguments to pass to the action.
            :param auth: The authentication parameter to use when making a request on the remote action.
            :param headers: The headers to use when making the request on the remote action.

            :returns: Returns a dictionary which contains the returned response data.
        """
        rtnval = None

        completion_interval = aspects.completion_interval
        completion_timeout = aspects.completion_timeout
        inactivity_interval = aspects.inactivity_interval
        inactivity_timeout = aspects.inactivity_timeout
        monitor_delay = aspects.monitor_delay

        this_thr = threading.current_thread()
        monmsg= "Thread failed to exit monitored scope. thid={} thname={} action_name={}".format(this_thr.ident, this_thr.name, action_name)

        if aspects.action_pattern == ActionPattern.SINGULAR:
            with MonitoredScope("CALL_ACTION-SINGULAR", monmsg, timeout=inactivity_timeout + monitor_delay) as _:
                rtnval = self._proxy_call_action(action_name, arguments=arguments, auth=auth, headers=headers, aspects=aspects)

        elif aspects.action_pattern == ActionPattern.DO_UNTIL_SUCCESS:
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=aspects.completion_timeout)

            while True:

                with MonitoredScope("CALL_ACTION-DO_UNTIL_SUCCESS", monmsg, timeout=inactivity_timeout + monitor_delay) as _:
                    try:
                        rtnval = self._proxy_call_action(action_name, arguments=arguments, auth=auth, headers=headers, aspects=aspects)
                        break
                    except Exception as xcpt:
                        pass

                now_time = datetime.now()
                if now_time > end_time:
                    elapsed = now_time - start_time
                    tomsg_lines = [
                        "Timeout waiting for UPNP action call success. start={} end={} now={} elapsed={}".format(start_time, end_time, now_time, elapsed),
                        "ACTION: %s" % action_name
                    ]
                    raise AKitTimeoutError(os.linesep.join(tomsg_lines)) from None

                time.sleep(completion_interval)

        elif aspects.action_pattern == ActionPattern.DO_WHILE_SUCCESS:
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=aspects.completion_timeout)

            while True:

                with MonitoredScope("CALL_ACTION-DO_WHILE_SUCCESS", monmsg, timeout=inactivity_timeout + monitor_delay) as _:
                    try:
                        rtnval = self._proxy_call_action(action_name, arguments=arguments, auth=auth, headers=headers, aspects=aspects)
                    except Exception as xcpt:
                        break

                now_time = datetime.now()
                if now_time > end_time:
                    elapsed = now_time - start_time
                    tomsg_lines = [
                        "Timeout waiting for UPNP action call failure. start={} end={} now={} elapsed={}".format(start_time, end_time, now_time, elapsed),
                        "ACTION: %s" % action_name
                    ]
                    raise AKitTimeoutError(os.linesep.join(tomsg_lines)) from None

                time.sleep(completion_interval)
        else:
            errmsg = "UpnpServiceProxy: Unknown ActionPattern encountered. action_pattern={}".format(aspects.action_pattern)
            raise AKitRuntimeError(errmsg) from None

        return rtnval

    def lookup_default_variable(self, varname: str) -> Union[UpnpDefaultVar, None]:
        """
            Looks up the specified default variable.

            :param varname: The event name to find the :class:`UpnpDefaultVar` for.
        """
        varobj = None

        varkey = "{}/{}".format(self.SERVICE_TYPE, varname)

        self._service_lock.acquire()
        try:
            if varkey in self._default_variables:
                varobj = self._default_variables[varkey]
        finally:
            self._service_lock.release()

        return varobj

    def lookup_event_variable(self, eventname: str) -> Union[UpnpEventVar, None]:
        """
            Looks up the specified event variable.

            :param eventname: The event name to find the :class:`UpnpEventVar` for.
        """
        varobj = None

        varkey = "{}/{}".format(self.SERVICE_TYPE, eventname)

        self._service_lock.acquire()
        try:
            if varkey in self._evented_variables:
                varobj = self._evented_variables[varkey]
        finally:
            self._service_lock.release()

        return varobj

    def notify_byebye(self) -> bool:
        self._service_lock.acquire()
        try:
            self._subscription_id = None
            self._subscription_expiration = None

            for varkey in self._evented_variables:
                varobj = self._evented_variables[varkey]
                varobj.notify_byebye()
        finally:
            self._service_lock.release()
        return

    def renew_subscription(self):
        self.device.unsubscribe_to_events(self)
        self.device.subscribe_to_events(self)
        return

    def yield_service_lock(self) -> threading.RLock:
        """
            Yields the service lock in a way that it can be automatically release at the end of an
            iteration scope.
        """
        self._service_lock.acquire()
        try:
            yield
        finally:
            self._service_lock.release()

    def _clear_subscription(self):
        self._service_lock.acquire()
        try:
            self._subscription_id = None
            self._subscription_expiration = None
        finally:
            self._service_lock.release()
        return

    def _create_default_variable(self, event_name: str, data_type: Optional[str] = None, default: Optional[str] = None, allowed_list: Optional[list] = None, evented: bool=True):
        """
            Creates a default variable and stores a reference to it in the variables table.

            :param event_name: The name of the event variable to create.
            :param data_type: The type of the event variable to create.
            :param default: The default value to set the new event variable to.
        """

        variable_key = "{}/{}".format(self.SERVICE_TYPE, event_name)

        service_ref = weakref.ref(self)
        event_var = UpnpEventVar(variable_key, event_name, service_ref, data_type=data_type, default=default, allowed_list=allowed_list, evented=evented)
        self._default_variables[variable_key] = event_var

        return

    def _create_event_variable(self, event_name: str, data_type: Optional[str] = None, default: Optional[str] = None, allowed_list: Optional[list] = None, evented: bool=True):
        """
            Creates an event variable and stores a reference to it in the variables table.

            :param event_name: The name of the event variable to create.
            :param data_type: The type of the event variable to create.
            :param default: The default value to set the new event variable to.
        """
        variable_key = "{}/{}".format(self.SERVICE_TYPE, event_name)

        service_ref = weakref.ref(self)
        event_var = UpnpEventVar(variable_key, event_name, service_ref, data_type=data_type, default=default, allowed_list=allowed_list, evented=evented)
        self._evented_variables[variable_key] = event_var

        return

    def _create_default_variables_from_list(self):
        """
            Called by the constructor to create the defalut variables listed in the SERVICE_DEFAULT_VARIABLES list on creation
            of the service proxy instance.  We pre-create the event variables because they can have default values and 
            we want to maintain consistent reference for the variables for the the life of the service instance.
        """
        for event_name in self.SERVICE_DEFAULT_VARIABLES:
            event_info = self.SERVICE_DEFAULT_VARIABLES[event_name]
            self._create_default_variable(event_name, **event_info)
        return

    def _create_event_variables_from_list(self):
        """
            Called by the constructor to create the event variables listed in the SERVICE_EVENT_VARIABLES list on creation
            of the service proxy instance.  We pre-create the event variables because they can have default values and 
            we want to maintain consistent reference for the variables for the the life of the service instance.
        """
        for event_name in self.SERVICE_EVENT_VARIABLES:
            event_info = self.SERVICE_EVENT_VARIABLES[event_name]
            self._create_event_variable(event_name, **event_info)
        return

    def _proxy_link_service_to_device(self, device_ref: weakref.ReferenceType, service_description: UpnpDevice1Service):
        """
            Called to link a :class:`UpnpServiceProxy` instance to a :class:`UpnpDevice` instance.  The link to the parent
            device allows device users to find the service instance and to link the service proxy with the host it interacts
            with.  It is also utilized by the service proxy to setup event subscription callback routing in order to be
            able to route updates to the :class:`UpnpEventVar` variables managed by this service proxy.

            :param device_ref: A weak reference to the parent device that owns this device.
            :param service_description: The service description for this service.
        """

        device = device_ref()

        self._device_ref = device_ref

        self._host = device.host
        self._baseURL = device.URLBase

        self._controlURL = service_description.controlURL
        self._eventSubURL = service_description.eventSubURL
        self._SCPDURL = service_description.SCPDURL
        self._serviceId = service_description.serviceId
        self._serviceType = service_description.serviceType

        return

    def _proxy_set_call_parameters(self, host: str, baseURL: str, controlURL: str, eventSubURL: str, serviceId: Optional[str] = None, serviceType: Optional[str] = None):
        """
            Sets the call parameters that are used by the service for making calls on a remote service.

            :param host: The host of the remote service.
            :param baseURL: The base URL of the host and remote service.
            :param controlURL: The URL use to make calls on service actions.
            :param eventSubURL: The URL to use for creating service event variable subscriptions.
            :param serviceId: The service ID of the service.
            :param serviceType: The service Type ID of the service.
        """
        self._host = host

        if serviceId is None:
            serviceId = self.SERVICE_ID

        if serviceType is None:
            serviceType = self.SERVICE_TYPE

        self._baseURL = baseURL

        self._controlURL = controlURL
        self._eventSubURL = eventSubURL
        self._serviceId = serviceId
        self._serviceType = serviceType
        return

    def _proxy_call_action(self, action_name: str, arguments: dict = {}, auth: Optional[dict] = None, headers: dict = {}, aspects: Aspects=DEFAULT_ASPECTS) -> dict:
        """
            Helper method utilize by derived service proxies to make calls on remote service actions.

            :param action_name: The action name to make a call on.
            :param arguments: The arguments to pass to the action.
            :param auth: The authentication parameter to use when making a request on the remote action.
            :param headers: The headers to use when making the request on the remote action.

            :returns: Returns a dictionary which contains the returned response data.
        """
        # pylint: disable=dangerous-default-value

        call_url = self.controlURL
        if self._baseURL is not None:
            call_url = self._baseURL + call_url

        call_body = self._soap_processor.create_request(action_name, arguments, typed=self.serviceType)

        call_headers = {
            'SOAPAction': '"%s#%s"' % (self.serviceType, action_name),
            'Host': self._host,
            'Content-Type': 'text/xml'
        }
        call_headers.update(headers)

        resp = None
        try:
            resp = requests.post(
                call_url,
                call_body,
                headers=call_headers,
                timeout=SOAP_TIMEOUT,
                auth=auth
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            if resp is not None:
                # If the body of the error response contains XML then it should be a UPnP error,
                # extract the UPnP error information and raise a UpnpError
                content_type = resp.headers["CONTENT-TYPE"]
                if content_type.find('text/xml') == -1:
                    raise
        except:
            errmsg = traceback.format_exc()
            print(errmsg)
            raise

        resp_content = resp.content.strip()

        resp_dict = None

        status_code = resp.status_code
        if status_code >= 200 and status_code < 300: # pylint: disable=chained-comparison
            resp_dict = self._soap_processor.parse_response(action_name, resp_content, typed=self.serviceType)
        else:
            errorCode, errorDescription = self._soap_processor.parse_response_error_for_upnp(action_name, resp_content, status_code, typed=self.serviceType)
            raise UpnpError(errorCode, errorDescription, "host=%s action=%s args=%s" % (self._host, action_name, repr(arguments)))

        return resp_dict

    def _update_event_variables(self, sender_ip, usn_dev, propertyNodeList):
        """
            Helper method called during the processing of a subscription callback in order
            to update all of the event variables for this service instance.

            :param propertyNodeList: An XML :class:`Element` object that contains a list
                                     of child elements for each event variable.
        """
        self._service_lock.acquire()
        try:
            for propNodeOuter in propertyNodeList:
                # Get the first node of the outer property node
                propNode = propNodeOuter.getchildren()[0]

                event_name = propNode.tag
                event_value = propNode.text

                if "AVTransport" in self.SERVICE_TYPE:
                    print("")

                var_key = "{}/{}".format(self.SERVICE_TYPE, event_name)

                if var_key in self._evented_variables:
                    varobj = self._evented_variables[var_key]
                    if self._logged_events is not None and event_name in self._logged_events:
                        infomsg = "UPNP event update for {}/{}/{} from {}{}    VALUE: {}".format(
                            usn_dev, self.SERVICE_TYPE, event_name, sender_ip, os.linesep, event_value)
                        logger.info(infomsg)
                    varobj.sync_update(event_value, service_locked=True)
                else:
                    self._service_lock.release()
                    try:
                        host = self._device_ref().host
                        logger.error("UpnpServiceProxy: Received value for unknown host=%s vkey=%s event=%s value=%r" % (host, var_key, event_name, event_value))
                    finally:
                        self._service_lock.acquire()
        finally:
            self._service_lock.release()

        return
