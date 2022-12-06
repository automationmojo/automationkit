
from typing import List, Optional

import os

from akit.exceptions import AKitCommandError, AKitHTTPRequestError, TracebackFormatPolicy
from akit.xformatting import format_command_result
import requests

__traceback_format_policy__ = TracebackFormatPolicy.Hide

def raise_for_command_status(status: int, stdout: str, stderr: str, context:str, exp_status: Optional[List[int]]=None):
    """
        Raises an :class:`AKitCommandError` if the status code is not what was expected.
    """

    if exp_status is None:
        exp_status = [0]

    if status not in exp_status:
        errmsg = format_command_result(context, status, stdout, stderr, exp_status=exp_status)
        raise AKitCommandError(errmsg, status, stdout, stderr)

    return

def raise_for_http_status(context: str, response: requests.Response, details: Optional[dict]=None, allow_redirects: bool=False):
    """
        Raises an :class:`AKitHTTPRequestError` if an HTTP response error occured.
    """

    status_code = response.status_code
    method = response.request.method
    req_url = response.url

    if status_code >= 400 or (not allow_redirects and status_code >= 300):
        err_msg_lines = [
            context
        ]

        reason = response.reason

        # If we have `bytes` then we need to decode it
        if isinstance(reason, bytes):
            try:
                reason = reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = reason.decode('iso-8859-1')

        if status_code < 400:
            # Client Error
            err_msg_lines.append("{} Redirect Error: {} for url: {} method: {}".format(
                status_code, reason, response.url, method))
        elif status_code < 500:
            # Client Error
            err_msg_lines.append("{} Client Error: {} for url: {} method: {}".format(
                status_code, reason, response.url, method))
        elif status_code >= 500 and status_code < 600:
            # Server Error
            err_msg_lines.append("{} Server Error: {} for url: {} method: {}".format(
                status_code, reason, response.url, method))
        else:
            err_msg_lines.append("{} UnExpected Error: {} for url: {} method: {}".format(
                status_code, reason, response.url, method))

        if details is not None:
            for dkey, dval in details.items():
                err_msg_lines.append("    {}: {}".format(dkey, dval))

        errmsg = os.linesep.join(err_msg_lines)
        raise AKitHTTPRequestError(errmsg, req_url, status_code, reason)

    return