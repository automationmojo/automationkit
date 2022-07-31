
from typing import Optional

import os

from akit.exceptions import AKitHTTPRequestError

import requests

def raise_for_status(self, context: str, response: requests.Response, details: Optional[dict]=None):
    """
        Raises an :class:`AKitHTTPRequestError` if an HTTP response error occured.
    """

    status_code = response.status_code
    method = response.request.method
    req_url = response.url

    if status_code >= 400:
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

        if status_code < 500:
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