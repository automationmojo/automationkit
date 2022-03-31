
from typing import List, Union

import os

from akit.exceptions import AKitAssertionError

def assert_api_list_length(api: str, to_inspect: List, expected_len: int) -> Union[AKitAssertionError, None]:
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

def assert_api_list_length_greater(api: str, to_inspect: List, boundary_len: int) -> Union[AKitAssertionError, None]:
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
    if found_len > boundary_len:

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

def assert_api_list_length_less(api: str, to_inspect: List, boundary_len: int) -> Union[AKitAssertionError, None]:
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
    if found_len < boundary_len:

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