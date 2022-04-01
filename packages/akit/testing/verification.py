from typing import Any, List, Optional, Union

import os

from pprint import pformat

from akit.xformatting import indent_lines

from akit.exceptions import AKitAssertionError


def api_assert_dict_response_has_keys(api: str, to_inspect: dict, expected_keys: List[str]) -> Union[AKitAssertionError, None]:
    """
        Verifies that the speicified return result from the specified API has the specified expected keys.  If the
        verification fails then an :class:`AKitAssertionError` is created and return, otherwise None is returned. It
        is the resposibility of the calling test to raise the returned error.

        :param api: The name of the API that returned the result being inspected.
        :param to_inspect: The dictionary being inspected
        :param expected_keys: The list of expected keys

        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    errinst = None

    template = "    '{}' key not found."

    content_errors = verify_dict_has_keys(to_inspect, expected_keys, template)
    if len(content_errors) > 0:
        err_msg_lines = [
            "'{}' API result verification failed with the following errors:".format(api)
        ]

        for nxtce in content_errors:
            err_msg_lines.append(nxtce)

        errmsg = os.linesep.join(err_msg_lines)
        errinst = AKitAssertionError(errmsg)

    return errinst

def api_assert_dict_response_has_paths(api: str, to_inspect: dict, expected_paths: List[str]) -> Union[AKitAssertionError, None]:
    """
        Verifies that the speicified return result from the specified API has the specified expected paths.  If the
        verification fails then an :class:`AKitAssertionError` is created and return, otherwise None is returned. It
        is the resposibility of the calling test to raise the returned error.

        :param api: The name of the API that returned the result being inspected.
        :param to_inspect: The dictionary being inspected
        :param expected_keys: The list of expected keys

        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    errinst = None

    template = "    '{}' path not found."

    content_errors = verify_dict_has_paths(to_inspect, expected_paths, template)
    if len(content_errors) > 0:
        err_msg_lines = [
            "'{}' API result verification failed with the following errors:".format(api)
        ]

        for nxtce in content_errors:
            err_msg_lines.append(nxtce)

        errmsg = os.linesep.join(err_msg_lines)
        errinst = AKitAssertionError(errmsg)

    return errinst


def api_assert_equal(api: str, found: Any, expected: Any) -> Union[AKitAssertionError, None]:
    """
        Verifies that the speicified return result from the specified API has the specified expected value.
        If the verification fails then an :class:`AKitAssertionError` is created and returned, otherwise None
        is returned. It is the resposibility of the calling test to raise the returned error.

        :param api: The name of the API that returned the result being inspected.
        :param found: The value to be compared
        :param expected: The expected length of the list

        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    errinst = None

    if found != expected:

        err_msg_lines = [
            "'{}' API result verification failed because the found value did not match expected value:".format(api),
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
        errinst = AKitAssertionError(errmsg)

    return errinst

def api_assert_greater(api: str, found: Any, boundary: Any) -> Union[AKitAssertionError, None]:
    """
        Verifies that the speicified return result from the specified API has a value greater than the
        boundary specified. If the verification fails then an :class:`AKitAssertionError` is created
        and returned, otherwise None is returned. It is the resposibility of the calling test to raise
        the returned error.

        :param api: The name of the API that returned the result being inspected.
        :param found: The value being compared
        :param boundry: The boundary value being compared against

        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    errinst = None

    if not found > boundary:

        err_msg_lines = [
            "'{}' API result verification failed because the found value was not greater than the boundary value:".format(api)
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
        errinst = AKitAssertionError(errmsg)

    return errinst

def api_assert_lessthan(api: str, found: Any, boundary: Any) -> Union[AKitAssertionError, None]:
    """
        Verifies that the speicified return result from the specified API has a value less than the
        boundary specified. If the verification fails then an :class:`AKitAssertionError` is created
        and returned, otherwise None is returned. It is the resposibility of the calling test to raise
        the returned error.

        :param api: The name of the API that returned the result being inspected.
        :param found: The value being compared
        :param boundry: The boundary value being compared against

        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    errinst = None

    if not found < boundary:

        err_msg_lines = [
            "'{}' API result verification failed because the found value was not less than the boundary value:".format(api)
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
        errinst = AKitAssertionError(errmsg)

    return errinst


def api_assert_list_length(api: str, to_inspect: List, expected_len: int) -> Union[AKitAssertionError, None]:
    """
        Verifies that the speicified return result from the specified API has the specified expected number of items.
        If the verification fails then an :class:`AKitAssertionError` is created and returned, otherwise None
        is returned. It is the resposibility of the calling test to raise the returned error.

        :param api: The name of the API that returned the result being inspected.
        :param to_inspect: The list being inspected
        :param expected_len: The expected length of the list

        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    errinst = None

    found_len = len(to_inspect)
    if found_len != expected_len:

        err_msg_lines = [
            "'{}' API result verification failed because the actual length ({}) did not match expected length ({}):".format(
                api, found_len, expected_len),
            "ITEMS:"
        ]

        for fitem in to_inspect:
            err_msg_lines.append("    {}".format(fitem))
        err_msg_lines.append("")

        errmsg = os.linesep.join(err_msg_lines)
        errinst = AKitAssertionError(errmsg)

    return errinst

def api_assert_list_length_greater(api: str, to_inspect: List, boundary_len: int) -> Union[AKitAssertionError, None]:
    """
        Verifies that the speicified return result from the specified API has more items than the specified expected
        number of items.  If the verification fails then an :class:`AKitAssertionError` is created and returned,
        otherwise None is returned. It is the resposibility of the calling test to raise the returned error.

        :param api: The name of the API that returned the result being inspected.
        :param to_inspect: The list being inspected
        :param boundary_len: The boundary that the list length should exceed.

        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    errinst = None

    found_len = len(to_inspect)
    if not found_len > boundary_len:

        err_msg_lines = [
            "'{}' API result verification failed because the actual length ({}) was not greater than the boundary length ({}):".format(
                api, found_len, boundary_len),
            "ITEMS:"
        ]

        for fitem in to_inspect:
            err_msg_lines.append("    {}".format(fitem))
        err_msg_lines.append("")

        errmsg = os.linesep.join(err_msg_lines)
        errinst = AKitAssertionError(errmsg)

    return errinst

def api_assert_list_length_less(api: str, to_inspect: List, boundary_len: int) -> Union[AKitAssertionError, None]:
    """
        Verifies that the speicified return result from the specified API has less items than the specified expected
        number of items.  If the verification fails then an :class:`AKitAssertionError` is created and returned,
        otherwise None is returned. It is the resposibility of the calling test to raise the returned error.

        :param api: The name of the API that returned the result being inspected.
        :param to_inspect: The list being inspected
        :param boundary_len: The boundary the list length should not exceed

        :returns: None or an :class:`AKitAssertionError` for the caller to raise.
    """
    errinst = None

    found_len = len(to_inspect)
    if not found_len < boundary_len:

        err_msg_lines = [
            "'{}' API result verification failed because the actual length ({}) was not less than the boundary length ({}):".format(
                api, found_len, boundary_len),
            "ITEMS:"
        ]

        for fitem in to_inspect:
            err_msg_lines.append("    {}".format(fitem))
        err_msg_lines.append("")

        errmsg = os.linesep.join(err_msg_lines)
        errinst = AKitAssertionError(errmsg)

    return errinst

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

