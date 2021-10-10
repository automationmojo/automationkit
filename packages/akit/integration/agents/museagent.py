
import base64
import http
import os
import socket
import weakref

from html.parser import HTMLParser

import requests

from akit.aspects import ActionPattern, DEFAULT_ASPECTS
from akit.exceptions import AKitHTTPRequestError

from akit.integration.landscaping.landscapedeviceextension import LandscapeDeviceExtension

class HEADER_NAMES:
    AUTHORIZATION = "authorization"
    CONTENT_TYPE = "content-type"

CONTENT_TYPE_JSON = "applicaion/json"
CONTENT_TYPE_WWW_FORM_URLENCODED = "application/x-www-form-urlencoded;charset=utf-8"

REDIRECT_URI = "https://0.0.0.0:5000/callback"

class MuseAgent(LandscapeDeviceExtension):

    def __init__(self, envlabel, authhost, ctlhost, host, username, password, apikey, secret, bearer=None, version="v3", port=1443, verify=False, aspects=DEFAULT_ASPECTS):
        super(MuseAgent, self).__init__()

        self._envlabel = envlabel
        self._authhost = authhost
        self._ctlhost = ctlhost
        self._host = host
        self._ipaddr = socket.gethostbyname(self._host)
        self._port = port
        self._username = username
        self._password = password
        self._apikey = apikey
        self._secret = secret
        self._bearer_token = None
        self._version = version
        self._aspects = aspects
        self._verify = verify

        self._basic_auth = self._generate_basic_auth()

        #if self._bearer_token is None:
        #    self._bearer_token = self.auth_get_bearer_token()
        return

    @property
    def apikey(self):
        return self._apikey

    @property
    def aspects(self):
        return self._aspects

    @property
    def envlabel(self):
        return self._envlabel

    @property
    def envhost(self):
        return self._authhost

    @property
    def host(self):
        return self._host

    @property
    def ipaddr(self):
        return self._ipaddr

    @property
    def password(self):
        return self._password

    @property
    def secret(self):
        return self._secret

    @property
    def verify(self):
        return self._verify

    @property
    def version(self):
        return self._version

    def initialize(self, coord_ref: weakref.ReferenceType, basedevice_ref: weakref.ReferenceType, extid: str, location: str, configinfo: dict):
        """
            Initializes the landscape device extension.

            :param coord_ref: A weak reference to the coordinator that is managing interactions through this
                              device extension.
            :param extid: A unique reference that can be used to identify this device via the coordinator even if its location changes.
            :param location: The location reference where this device can be found via the coordinator.
            :param configinfo: The muse configuration information dictionary for the associated device from the landscape file.
        """
        LandscapeDeviceExtension.initialize(self, coord_ref, basedevice_ref, extid, location, configinfo)
        return

    def auth_get_bearer_token(self):

        # TODO: Fix the bearer token acquisition code
        leafurl = "/auth/oauth/v3/token"

        headers = {
            HEADER_NAMES.AUTHORIZATION: self._basic_auth
        }

        params = {
            "grant_type": "password",
            "password": self._password,
            "username": self._username,
            "scope": "hh-config-admin"
        }

        resp, _ = self._https_get(self._authhost, leafurl, params=params, headers=headers,
                                  cont_type=CONTENT_TYPE_WWW_FORM_URLENCODED)
        if resp.status_code == 200:
            content = resp.content.decode("utf-8")
            csrfToken = self._extract_csrf_token(content)
            params["csrfToken"] = csrfToken

            resp2, _ = self._https_post(self._authhost, leafurl, params=params, headers=headers,
                                  cont_type=CONTENT_TYPE_WWW_FORM_URLENCODED)
            if resp2.status_code == 200:
                print (resp2.content)
                print ()

        return

    def households(self):
        leafurl = "/control/api/{}/households".format(self._version)

        headers = {
            HEADER_NAMES.AUTHORIZATION: self._bearer_token
        }

        resp, resp_obj = self._https_get(self._ctlhost, leafurl, params=None, headers=headers,
                                  cont_type=CONTENT_TYPE_WWW_FORM_URLENCODED)
        if resp.status_code == 200:
            print (resp_obj)
            print ()

        return

    def refresh_credentials(self):
        self._bearer_token = self.auth_get_bearer_token()
        return

    def _extract_csrf_token(self, content):
        csrfToken = None

        class CsrfTokenParser(HTMLParser):

            def __init__(self, *args, **kwargs):
                super(CsrfTokenParser, self).__init__(*args, **kwargs)
                self.csrfToken = None
                return

            def handle_starttag(self, tag, attrs):
                if tag == "input":
                    attrs = dict(attrs)
                    if "id" in attrs and "value" in attrs:
                        id = attrs["id"]
                        if id == "csrf-token":
                            self.csrfToken = attrs["value"]

        csrfParser = CsrfTokenParser()
        csrfParser.feed(content)

        if csrfParser.csrfToken is not None:
            csrfToken = csrfParser.csrfToken

        return csrfToken

    def _generate_basic_auth(self):
        auth_code = "{}:{}".format(self._apikey, self._secret).encode("ascii")
        auth_code_b64 = base64.b64encode(auth_code)
        auth_header = "Basic {}".format(auth_code_b64.decode('ascii'))
        return auth_header

    def _https_get(self, host, leafurl, port=None, params=None, body=None, headers=None, timeout=None,
                   allow_raise=True, allow_redirects=False, cont_type=CONTENT_TYPE_JSON,
                   exp_resp_type=CONTENT_TYPE_JSON, exp_status=[http.HTTPStatus.OK]):

        resp, resp_boj = self._http_transact("GET", "https", host, leafurl, port=port, params=params, body=body, headers=headers,
                                             timeout=timeout, allow_raise=allow_raise, allow_redirects=allow_redirects,
                                             cont_type=cont_type, exp_resp_type=exp_resp_type, exp_status=exp_status)

        return resp, resp_boj

    def _https_post(self, host, leafurl, port=None, params=None, body=None, headers=None, timeout=None,
                   allow_raise=True, allow_redirects=False, cont_type=CONTENT_TYPE_JSON,
                   exp_resp_type=CONTENT_TYPE_JSON, exp_status=[http.HTTPStatus.OK]):

        resp, resp_boj = self._http_transact("POST", "https", host, leafurl, port=port, params=params, body=body, headers=headers,
                                             timeout=timeout, allow_raise=allow_raise, allow_redirects=allow_redirects,
                                             cont_type=cont_type, exp_resp_type=exp_resp_type, exp_status=exp_status)

        return resp, resp_boj

    def _http_transact(self, method,  scheme, host, leafurl, port=None, params=None, body=None, headers=None,
                       timeout=None, allow_raise=True, allow_redirects=False, cont_type=CONTENT_TYPE_JSON,
                       exp_resp_type=CONTENT_TYPE_JSON, exp_status=[http.HTTPStatus.OK]):

        port_fill = ""
        if port is not None:
            port_fill = ":%d" % port


        requrl = "{}://{}{}{}".format(scheme, host, port_fill, leafurl)

        update_headers = None
        if cont_type is not None:
            update_headers = {
                HEADER_NAMES.CONTENT_TYPE: cont_type
            }

        if headers is not None and update_headers is not None:
            headers.update(update_headers)

        req = requests.Request(method, requrl, params=params, data=body, headers=headers)

        prereq = req.prepare()

        session = requests.Session()

        resp_obj = None
        resp = session.send(prereq, timeout=timeout, verify=self._verify)
        if resp.status_code in exp_status:
            resp_type = None
            if "Content-Type" in resp.headers:
                resp_type = resp.headers["Content-Type"]

            if resp_type == CONTENT_TYPE_JSON:
                resp_obj = resp.json()
        elif allow_raise:
            errmsg_lines = [
                "Muse API Request Failure",
                "    requrl={}".format(requrl)
            ]
            errmsg = os.linesep.join(errmsg_lines)
            raise AKitHTTPRequestError(errmsg) from None

        return resp, resp_obj
