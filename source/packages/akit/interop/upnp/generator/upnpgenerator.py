
"""
.. module:: upnpgenerator
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that processes service descriptions and generates proxy service wrappers used
               to communicated with UPNP services.

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

from typing import Optional, Tuple, Union

import os
import sys

from argparse import ArgumentParser, ArgumentError

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring as xml_fromstring

from akit.paths import ensure_directory_is_package

from akit.interop.coordinators.upnpcoordinator import UpnpCoordinator

# pylint: disable=unused-import

UPNP_SERVICE_NAMESPACE = "urn:schemas-upnp-org:service-1-0"

MANUFACTURER_TO_BASE_CLASSES = {
    'SonosInc': ("akit.interop.upnp.devices.embedded.upnpdevice", "SonosDevice")
}

CONTENT_PROXY_FILE_HEADER = """
    NOTE: This is a code generated file.  This file should not be edited directly.
"""

TEMPLATE_CLASS_PREFIX = """

from akit.aspects import AspectsUPnP, DEFAULT_UPNP_ASPECTS

from akit.extensible import LoadableExtension
from akit.interop.upnp.services.upnpserviceproxy import UpnpServiceProxy

class %(class_name)s(UpnpServiceProxy, LoadableExtension):
    \"""
        This is a code generated proxy class to the '%(class_name_base)s' service.
    \"""

    SERVICE_MANUFACTURER = '%(service_manufacturer)s'
    SERVICE_TYPE = '%(service_type)s'

    SERVICE_DEFAULT_VARIABLES = {%(svc_default_vars)s}

    SERVICE_EVENT_VARIABLES = {%(svc_event_vars)s}
"""

TEMPLATE_ACTION_NO_RETURN = """
    def action_%(action_name)s(self%(in_params_comma)s%(in_params_list)s, *, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        \"""
            Calls the %(action_name)s action.
        \"""
        arguments = %(args_dict)s

        self.call_action("%(action_name)s", arguments=arguments, aspects=aspects)

        return
"""

TEMPLATE_ACTION_WITH_RETURN = """
    def action_%(action_name)s(self%(in_params_comma)s%(in_params_list)s, *, extract_returns=True, aspects:AspectsUPnP=DEFAULT_UPNP_ASPECTS):
        \"""
            Calls the %(action_name)s action.

            :returns: %(out_params_list)s
        \"""
        arguments = %(args_dict)s

        out_params = self.call_action("%(action_name)s", arguments=arguments, aspects=aspects)

        rtn_args = out_params
        if extract_returns:
            rtn_args = [out_params[k] for k in (%(out_params_list)s,)]
            if len(rtn_args) == 1:
                rtn_args = rtn_args[0]

        return rtn_args
"""

def node_lower_strip_text(txt: Union[str, None]) -> Union[str, None]:
    """
        Converts text to lower case and strips leading and trailing whitespace if not None.

        :param txt: The text to convert to lower case and to strip.
    """
    if txt is not None:
        txt = txt.lower().strip()
    return txt

def node_strip_text(txt: Union[str, None]) -> Union[str, None]:
    """
        Strips leading and trailing whitespace from the given text if not None.

        :param txt: The text to strip.
    """
    if txt is not None:
        txt = txt.strip()
    return txt

def generate_upnp_service_proxy(servicesDir: str, serviceManufacturer: str, serviceType: str, variablesTable: dict, typesTable: dict, eventsTable: dict, actionsTable: dict):
    """
        Generates a service proxy using the parameters provided.

        :param servicesDir: The directory to output the service proxy to.
        :param serviceManufacturer: The name of the manufacturer for the device that a service proxy is being generated for.
        :param serviceType: The name of the service type that a service proxy is being generated for.
        :param variablesTable: A table containing the information about the variables associated with a service.
        :param typesTable: A table containing the types associated with the variables used by the service.
        :param eventsTable: A table containing information about the events published by the services.
        :param actionsTable: A table containing information about the actions that can be called on the service.

    """
    # pylint: disable=unused-argument

    if not os.path.exists(servicesDir):
        os.makedirs(servicesDir)

    ensure_directory_is_package(servicesDir, package_title="Services directory module")

    service_type_parts = serviceType.split(":")

    class_name_base = service_type_parts[3] + service_type_parts[-1]
    class_name = class_name_base + "ServiceProxy"
    file_base = class_name.lower() + ".py"

    service_variables_content = ""

    class_fill_dict = {
        "class_name": class_name,
        "class_name_base": class_name_base,
        "service_manufacturer": serviceManufacturer,
        "service_type": serviceType,
        "service_variables": service_variables_content
    }

    manufacturerDir = os.path.join(servicesDir, serviceManufacturer)
    if not os.path.exists(manufacturerDir):
        os.makedirs(manufacturerDir)

    dest_file_full = os.path.join(manufacturerDir, file_base)


    variable_names_sorted = [ k for k in variablesTable.keys() ]
    variable_names_sorted.sort()

    event_variable_lines = []
    default_variable_lines = []

    for var_name in variable_names_sorted:
        variable_info = variablesTable[var_name]

        var_name = variable_info["name"]
        var_type = variable_info["dataType"]
        var_send_events = variable_info["sendEvents"]

        var_allowed_list = None
        if "allowedValueList" in variable_info:
            var_allowed_list = variable_info["allowedValueList"]

        var_default_value = None
        if "defaultValue" in variable_info:
            var_default_value = variable_info["defaultValue"]

        default_entry = ", \"default\": None"
        if var_default_value is not None:
            default_entry = ", \"default\": \"%s\"" % var_default_value

        allowed_list_entry = ", \"allowed_list\": None"
        if var_allowed_list is not None:
            allowed_list_entry = ", \"allowed_list\": \"%s\"" % var_allowed_list

        if var_send_events == 'yes':
            table_var_line = "\"%s\": { \"data_type\": \"%s\"%s%s},\n" % (var_name, var_type, default_entry, allowed_list_entry)
            event_variable_lines.append(table_var_line)
        else:
            table_var_line = "\"%s\": { \"data_type\": \"%s\"%s%s},\n" % (var_name, var_type, default_entry, allowed_list_entry)
            default_variable_lines.append(table_var_line)

    if len(event_variable_lines) > 0:
        service_variables_content = "\n        " + "        ".join(event_variable_lines) + "    "
        class_fill_dict["svc_event_vars"] = service_variables_content
    else:
        class_fill_dict["svc_event_vars"] = ""

    if len(default_variable_lines) > 0:
        service_variables_content = "\n        " + "        ".join(default_variable_lines) + "    "
        class_fill_dict["svc_default_vars"] = service_variables_content
    else:
        class_fill_dict["svc_default_vars"] = ""

    with open(dest_file_full, 'w') as spf:
        spf.write('"""\n')
        spf.write(CONTENT_PROXY_FILE_HEADER)
        spf.write('"""\n')
        spf.write('\n')
        spf.write(TEMPLATE_CLASS_PREFIX % class_fill_dict)

        action_names_sorted = [ k for k in actionsTable.keys() ]
        action_names_sorted.sort()

        for action_name in action_names_sorted:

            action_info = actionsTable[action_name]

            in_params_list = ""
            out_params_list = ""

            args_dict = "{ }"
            args_in_keys = action_info["args_in_keys"]
            if len(args_in_keys) > 0:
                in_params_list = ", ".join(args_in_keys)
                args_dict = "{\n"
                for arg_key in args_in_keys:
                    args_dict += '            "%s": %s,\n' % (arg_key, arg_key)
                args_dict += "        }"

            in_params_comma = ""
            if len(in_params_list) > 0:
                in_params_comma = ", "

            args_out_keys = [ '"%s"' % ok for ok in action_info["args_out_keys"] ]
            if len(args_out_keys) > 0:
                out_params_list = ", ".join(args_out_keys)

            action_fill = {
                "action_name": action_name,
                "in_params_list": in_params_list,
                "in_params_comma": in_params_comma,
                "out_params_list": out_params_list,
                "args_dict": args_dict
            }
            if len(out_params_list) > 0:
                spf.write(TEMPLATE_ACTION_WITH_RETURN % action_fill)
            else:
                spf.write(TEMPLATE_ACTION_NO_RETURN % action_fill)

    return

def process_action_list(svcActionListNode: Element, namespaces: Optional[dict] = None) -> dict:
    """
        Processes the action list node for a service description and creates a table with all the actions available
        on the service.

        :param svcActionListNode: The action list xml node from the serivce description document.
        :param namespace: The namespace to use when processing the XML dom nodes.

        :returns: Returns a table of actions supported by the service.
    """
    actionsTable = {}

    actionNodeList = svcActionListNode.findall("action", namespaces=namespaces)
    for actionNode in actionNodeList:
        action_name = node_strip_text(actionNode.find("name", namespaces=namespaces).text)
        args_in_keys = []
        args_in_table = {}
        args_out_keys = []
        args_out_table = {}

        argumentListNode = actionNode.find("argumentList", namespaces=namespaces)
        if argumentListNode is not None:
            argumentNodeList = argumentListNode.findall("argument", namespaces=namespaces)
            for argumentNode in argumentNodeList:
                arg_info = {}
                arg_name = node_strip_text(argumentNode.find("name", namespaces=namespaces).text)
                arg_direction = node_lower_strip_text(argumentNode.find("direction", namespaces=namespaces).text)

                arg_related = None
                argRelatedNode = argumentNode.find("relatedStateVariable", namespaces=namespaces)
                if argRelatedNode is not None:
                    arg_related = node_strip_text(argRelatedNode.text)

                arg_info["name"] = arg_name
                arg_info["direction"] = arg_direction
                arg_info["relatedStateVariable"] = arg_related

                if arg_direction == "in":
                    args_in_keys.append(arg_name)
                    args_in_table[arg_name] = arg_info
                elif arg_direction == "out":
                    args_out_keys.append(arg_name)
                    args_out_table[arg_name] = arg_info
                else:
                    raise ValueError("Invalid argument direction %s" % arg_direction)

        action_info = {
            "name": action_name,
            "args_in": args_in_table,
            "args_in_keys": args_in_keys,
            "args_out": args_out_table,
            "args_out_keys": args_out_keys
        }

        actionsTable[action_name] = action_info

    return actionsTable

def process_service_state_table(svcStateTableNode: Element, namespaces: Optional[dict] = None) -> Tuple[dict, dict, dict]:
    """
        Processes the action list node for a service description and creates a table with all the actions available
        on the service.

        :param svcStateTableNode: The state table XML node from the serivce description document.
        :param namespace: The namespace to use when processing the XML dom nodes.

        :returns: Returns tables for the variables, types and events supported by the service.
    """
    variablesTable = {}
    typesTable = {}
    eventsTable = {}

    stateVariableNodeList = svcStateTableNode.findall("stateVariable", namespaces=namespaces)

    for stateVariableNode in stateVariableNodeList:

        variable_info = {}

        var_name = node_strip_text(stateVariableNode.find("name", namespaces=namespaces).text)
        variable_info["name"] = var_name

        send_events = "no"
        if "sendEvents" in stateVariableNode.attrib:
            send_events = node_lower_strip_text(stateVariableNode.attrib["sendEvents"])
        else:
            sendEventsNode = stateVariableNode.find("sendEventsAttribute")
            if sendEventsNode is not None:
                send_events = node_lower_strip_text(sendEventsNode.text)

        variable_info["sendEvents"] = send_events


        var_type = stateVariableNode.find("dataType", namespaces=namespaces).text.strip()
        variable_info["dataType"] = var_type

        allowedValueListNode = stateVariableNode.find("allowedValueList", namespaces=namespaces)
        if allowedValueListNode is not None:
            allowed_value_list = []
            for allowedValueNode in allowedValueListNode.findall("allowedValue", namespaces=namespaces):
                allowed_value = node_strip_text(allowedValueNode.text)
                allowed_value_list.append(allowed_value)
            variable_info["allowedValueList"] = allowed_value_list

        defaultValueNode = stateVariableNode.find("defaultValue", namespaces=namespaces)
        if defaultValueNode is not None:
            default_value = node_strip_text(defaultValueNode.text)
            variable_info["defaultValue"] = default_value

        if var_name.startswith("A_ARG_TYPE_"):
            typesTable[var_name] = variable_info
        else:
            variablesTable[var_name] = variable_info
            if send_events == "yes":
                eventsTable[var_name] = variable_info

    return variablesTable, typesTable, eventsTable


def generate_service_proxies(svc_desc_directory: str, svc_proxy_directory: str):
    """
        Processes the XML service description documents in the description documents folder and generates the
        service proxy modules.  Then outputs the generated proxy modules to the service proxy foloder specified.

        :param svc_desc_directory: The directory that contains the service description documents to process.
        :param svc_proxy_directory: The directory that is the output directory for the service proxy modules.
    """
    for dirpath, _, filenames in os.walk(svc_desc_directory, topdown=True):
        for nxtfile in filenames:

            serviceType, nxtfile_ext = os.path.splitext(nxtfile)
            if nxtfile_ext != ".xml":
                continue

            serviceManufacturer = os.path.basename(dirpath)

            svc_content = None

            fullpath = os.path.join(dirpath, nxtfile)
            with open(fullpath, 'r') as xf:
                svc_content = xf.read()

            docNode = xml_fromstring(svc_content)
            if docNode is not None:

                namespaces = None
                doc_node_tag = docNode.tag
                if doc_node_tag.find("}") > 0:
                    default_ns = doc_node_tag[doc_node_tag.find("{") + 1:doc_node_tag.find("}")]
                    namespaces = {"": default_ns}

                variablesTable = {}
                typesTable = {}
                eventsTable = {}

                svcStateTableNode = docNode.find("serviceStateTable", namespaces=namespaces)
                if svcStateTableNode is not None:
                    variablesTable, typesTable, eventsTable = process_service_state_table(svcStateTableNode, namespaces=namespaces)

                if serviceType.find("DeviceProperties") > 0:
                    print("found")

                actionsTable = {}
                actionListNode = docNode.find("actionList", namespaces=namespaces)
                if actionListNode is not None:
                    actionsTable = process_action_list(actionListNode, namespaces=namespaces)

                generate_upnp_service_proxy(svc_proxy_directory, serviceManufacturer, serviceType, variablesTable, typesTable, eventsTable, actionsTable)
            else:
                errmsg = "WARNING: No serice node found in file:\n    %s\n" % fullpath
                print(errmsg, file=sys.stderr)

    return
