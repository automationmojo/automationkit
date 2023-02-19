from distutils.sysconfig import PREFIX
from typing import Any, List, Optional, Union, Type

import os
import re

from pprint import pformat

from akit.xformatting import indent_lines

from akit.exceptions import AKitAssertionError, TracebackFormatPolicy

__traceback_format_policy__ = TracebackFormatPolicy.Hide

PREFIX_STD = "Result"
PREFIX_API = "'{}' API result"

def assert_dict_response_has_keys(to_inspect: dict, expected_keys: List[str], api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has the specified expected keys.  If the
        verification fails then an :class:`AKitAssertionError` is created and return, otherwise None is returned. It
        is the resposibility of the calling test to raise the returned error.

        :param to_inspect: The dictionary being inspected
        :param expected_keys: The list of expected keys
        :param api: The optional name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    template = "    '{}' key not found."

    content_errors = verify_dict_has_keys(to_inspect, expected_keys, template)
    if len(content_errors) > 0:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed with the following errors:".format(msg_prefix)
        ]

        for nxtce in content_errors:
            err_msg_lines.append(nxtce)

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return

def assert_dict_response_has_paths(to_inspect: dict, expected_paths: List[str], api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has the specified expected paths.  If the
        verification fails then an :class:`AKitAssertionError` is created and return, otherwise None is returned. It
        is the resposibility of the calling test to raise the returned error.

        :param to_inspect: The dictionary being inspected
        :param expected_keys: The list of expected keys
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    template = "    '{}' path not found."

    content_errors = verify_dict_has_paths(to_inspect, expected_paths, template)
    if len(content_errors) > 0:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed with the following errors:".format(msg_prefix)
        ]

        for nxtce in content_errors:
            err_msg_lines.append(nxtce)

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return


def assert_equal(found: Any, expected: Any, api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has the specified expected value.
        If the verification fails then an :class:`AKitAssertionError` is created and returned, otherwise None
        is returned. It is the resposibility of the calling test to raise the returned error.

        :param found: The value to be compared
        :param expected: The expected value
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    if found != expected:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed because the found value did not match expected value:".format(msg_prefix),
            "EXPECTED:"
        ]

        exp_format_lines = pformat(expected, indent=4).strip().splitlines()
        if len(exp_format_lines) == 1:
            err_msg_lines.append("EXPECTED: {}".format(exp_format_lines[0]))
        elif len(exp_format_lines) > 1:
            err_msg_lines.append("EXPECTED:")
            exp_format_lines = indent_lines(exp_format_lines, 1)
            err_msg_lines.extend(exp_format_lines)

        found_format_lines = pformat(found, indent=4).splitlines()
        if len(found_format_lines) == 1:
            err_msg_lines.append("FOUND: {}".format(found_format_lines[0]))
        elif len(found_format_lines) > 1:
            err_msg_lines.append("FOUND:")
            found_format_lines = indent_lines(found_format_lines, 1)
            err_msg_lines.extend(found_format_lines)

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return

def assert_expression(found: str, expr: Union[str, re.Pattern], api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has the specified expected value.
        If the verification fails then an :class:`AKitAssertionError` is created and returned, otherwise None
        is returned. It is the resposibility of the calling test to raise the returned error.

        :param found: The value to be compared
        :param expr: An expression to match with the found value.
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    if not isinstance(expr, re.Pattern):
        expr = re.compile(expr)

    mobj = expr.match(found)
    if mobj is None:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed because the found value did not match expression provided.".format(msg_prefix),
            "FOUND: {}".format(found),
            "EXPR: {}".format(expr)
        ]

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return

def assert_greater(found: Any, boundary: Any, api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has a value greater than the
        boundary specified. If the verification fails then an :class:`AKitAssertionError` is created
        and returned, otherwise None is returned. It is the resposibility of the calling test to raise
        the returned error.

        :param found: The value being compared
        :param boundry: The boundary value being compared against
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    if not found > boundary:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed because the found value was not greater than the boundary value:".format(msg_prefix)
        ]

        bndry_format_lines = pformat(boundary, indent=4).strip().splitlines()
        if len(bndry_format_lines) == 1:
            err_msg_lines.append("BOUNDARY: {}".format(bndry_format_lines[0]))
        elif len(bndry_format_lines) > 1:
            err_msg_lines.append("BOUNDARY:")
            bndry_format_lines = indent_lines(bndry_format_lines, 1)
            err_msg_lines.extend(bndry_format_lines)

        found_format_lines = pformat(found, indent=4).splitlines()
        if len(found_format_lines) == 1:
            err_msg_lines.append("FOUND: {}".format(found_format_lines[0]))
        elif len(found_format_lines) > 1:
            err_msg_lines.append("FOUND:")
            found_format_lines = indent_lines(found_format_lines, 1)
            err_msg_lines.extend(found_format_lines)

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return

def assert_lessthan(found: Any, boundary: Any, api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has a value less than the
        boundary specified. If the verification fails then an :class:`AKitAssertionError` is created
        and returned, otherwise None is returned. It is the resposibility of the calling test to raise
        the returned error.

        :param found: The value being compared
        :param boundry: The boundary value being compared against
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    if not found < boundary:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed because the found value was not less than the boundary value:".format(msg_prefix)
        ]

        bndry_format_lines = pformat(boundary, indent=4).strip().splitlines()
        if len(bndry_format_lines) == 1:
            err_msg_lines.append("BOUNDARY: {}".format(bndry_format_lines[0]))
        elif len(bndry_format_lines) > 1:
            err_msg_lines.append("BOUNDARY:")
            bndry_format_lines = indent_lines(bndry_format_lines, 1)
            err_msg_lines.extend(bndry_format_lines)

        found_format_lines = pformat(found, indent=4).splitlines()
        if len(found_format_lines) == 1:
            err_msg_lines.append("FOUND: {}".format(found_format_lines[0]))
        elif len(found_format_lines) > 1:
            err_msg_lines.append("FOUND:")
            found_format_lines = indent_lines(found_format_lines, 1)
            err_msg_lines.extend(found_format_lines)

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return


def assert_list_length(to_inspect: List, expected_len: int, api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has the specified expected number of items.
        If the verification fails then an :class:`AKitAssertionError` is created and returned, otherwise None
        is returned. It is the resposibility of the calling test to raise the returned error.

        :param to_inspect: The list being inspected
        :param expected_len: The expected length of the list
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    found_len = len(to_inspect)
    if found_len != expected_len:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed because the actual length ({}) did not match expected length ({}):".format(
                msg_prefix, found_len, expected_len),
            "ITEMS:"
        ]

        for fitem in to_inspect:
            err_msg_lines.append("    {}".format(fitem))
        err_msg_lines.append("")

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return

def assert_list_length_greater(to_inspect: List, boundary_len: int, api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has more items than the specified expected
        number of items.  If the verification fails then an :class:`AKitAssertionError` is created and returned,
        otherwise None is returned. It is the resposibility of the calling test to raise the returned error.

        :param to_inspect: The list being inspected
        :param boundary_len: The boundary that the list length should exceed.
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    found_len = len(to_inspect)
    if not found_len > boundary_len:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed because the actual length ({}) was not greater than the boundary length ({}):".format(
                msg_prefix, found_len, boundary_len),
            "ITEMS:"
        ]

        for fitem in to_inspect:
            err_msg_lines.append("    {}".format(fitem))
        err_msg_lines.append("")

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return

def assert_list_length_less(to_inspect: List, boundary_len: int, api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has less items than the specified expected
        number of items.  If the verification fails then an :class:`AKitAssertionError` is created and returned,
        otherwise None is returned. It is the resposibility of the calling test to raise the returned error.

        :param to_inspect: The list being inspected
        :param boundary_len: The boundary the list length should not exceed
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    
    found_len = len(to_inspect)
    if not found_len < boundary_len:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)
        
        err_msg_lines = [
            "{} result verification failed because the actual length ({}) was not less than the boundary length ({}):".format(
                msg_prefix, found_len, boundary_len),
            "ITEMS:"
        ]

        for fitem in to_inspect:
            err_msg_lines.append("    {}".format(fitem))
        err_msg_lines.append("")

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return


def assert_type(found: Any, exp_type: Type, api: Optional[str] = None):
    """
        Verifies that the specified return result from the specified API has the specified expected value type.
        If the verification fails then an :class:`AKitAssertionError` is created and returned, otherwise None
        is returned. It is the resposibility of the calling test to raise the returned error.

        :param found: The value to check the type of
        :param exp_type: The expected value type
        :param api: The name of the API that returned the result being inspected.
        
        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """

    found_type = type(found)
    if found_type != exp_type:

        msg_prefix = PREFIX_STD if api is None else PREFIX_API.format(api)

        err_msg_lines = [
            "{} verification failed because the found value did not the expected type={}.".format(msg_prefix, exp_type),
            "FOUND_TYPE: {}".format(found_type)
        ]

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitAssertionError(errmsg)

    return


def verify_dict_has_keys(to_inspect: dict, expected_keys: List[str], template: Optional[str]=None) -> List[str]:
    """
        Verifies that the expected keys are found in the dictionary provided.  Returns a list of
        any keys that are missing.

        :param to_inspect: The dictionary being inspected
        :param expected_keys: The list of expected keys
        :param template: Optional template to combine with the missing key names to
                         product error messages for missing keys.

        :returns: List of missing keys or error messages.
    """

    missing_list = []

    if template is not None:
        for exkey in expected_keys:
            if exkey not in to_inspect:
                missing_list.append(template.format(exkey))
    else:
        for exkey in expected_keys:
            if exkey not in to_inspect:
                missing_list.append(exkey)

    return missing_list

def verify_dict_has_paths(to_inspect: dict, expected_paths: List[str], template: Optional[str]=None) -> List[str]:
    """
        Verifies that the expected keys are found in the dictionary provided.  Returns a list of
        any keys that are missing.

        :param to_inspect: The dictionary being inspected
        :param expected_paths: The list of expected paths to leafs in a dictionary
        :param template: Optional template to combine with the missing key names to
                         product error messages for missing keys.

        :returns: List of missing keys or error messages.
    """

    missing_list = []

    for next_exp_path in expected_paths:
        next_exp_path = next_exp_path.strip("/")

        leaf_parts = []

    return missing_list

def _verify_dict_has_paths_descend(search_path: str, cursor: dict, leaf_parts: list):

    found = False

    cursor_path = "/".join(leaf_parts)

    for nxt_key in cursor.keys():
        nxt_path = cursor_path + "/" + nxt_key
        if nxt_path == search_path:
            found = True
        elif search_path.startswith(nxt_path):
            nxt_val = cursor[nxt_key]
            if isinstance(nxt_val, dict):
                desc_leaf_parts = [lp for lp in leaf_parts]
                desc_leaf_parts.extend(nxt_key)
                _verify_dict_has_paths_descend(search_path, nxt_val, desc_leaf_parts)

    return found

