
import os

import yaml

from akit.exceptions import AKitConfigurationError

from akit.paths import get_filename_for_credentials

from akit.xlogging.foundations import getAutomatonKitLogger

from akit.interop.credentials.basiccredential import BasicCredential
from akit.interop.credentials.sshcredential import SshCredential

logger = getAutomatonKitLogger()

class CredentialManager:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CredentialManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._credentials = {}

        self._initialize_credentials()
        return

    @property
    def credentials(self):
        return self._credentials

    def _initialize_credentials(self):
        """
        """

        credential_file = get_filename_for_credentials()
        if os.path.exists(credential_file):
            credential_info = None

            with open(credential_file, 'r') as lf:
                lfcontent = lf.read()
                credential_info = yaml.safe_load(lfcontent)

            try:
                credentials_list = credential_info["credentials"]
                errors, warnings = self._validate_credentials(credentials_list)

                if len(errors) == 0:
                    for credential in credentials_list:
                        if "identifier" not in credential:
                            raise AKitConfigurationError("Credential items in 'environment/credentials' must have an 'identifier' member.") from None
                        ident = credential["identifier"]

                        if "category" not in credential:
                            raise AKitConfigurationError("Credential items in 'environment/credentials' must have an 'category' member.") from None
                        category = credential["category"]

                        if category == "basic":
                            BasicCredential.validate(credential)
                            credobj = BasicCredential(**credential)
                            self._credentials[ident] = credobj
                        elif category == "ssh":
                            SshCredential.validate(credential)
                            credobj = SshCredential(**credential)
                            self._credentials[ident] = credobj
                        else:
                            warnmsg = "Unknown category '{}' found in credential '{}'".format(category, ident)
                            logger.warn(warnmsg)
                else:
                    errmsg_lines = [
                        "Errors found in credential file={}".format(credential_file),
                        "ERRORS:"
                    ]
                    for err in errors:
                        errmsg_lines.append("    {}".format(err))

                    errmsg_lines.append("WARNINGS:")
                    for warn in warnings:
                        errmsg_lines.append("    {}".format(warn))

                    errmsg = os.linesep.join(errmsg_lines)
                    raise AKitConfigurationError(errmsg)
            except KeyError:
                errmsg = "No 'credentials' field found in file={}".format(credential_file)
                raise AKitConfigurationError(errmsg)
        else:
            warnmsg = "Credential file not found. expected={}".format(credential_file)
            logger.warn(warnmsg)

        return

    def _validate_credentials(self, cred_list):
        errors = []
        warnings = []

        identifier_set = set()

        for cinfo in cred_list:
            if "identifier" in cinfo:
                identifier = cinfo["identifier"]
                if identifier in identifier_set:
                    errmsg = "Duplicate identifer found. identifier=%s" % identifier
                    errors.append(errmsg)
                else:
                    identifier_set.add(identifier)
            else:
                errmsg = "All credentials must have an identifier field. cinfo=%r" % cinfo
                errors.append(errmsg)

            if "category" in cinfo:
                category = cinfo["category"]
                if category == "basic":
                    child_errors, child_warnings =  self._validate_credential_basic(cinfo)
                    errors.extend(child_errors)
                    warnings.extend(child_warnings)
                elif category == "ssh":
                    child_errors, child_warnings =  self._validate_credential_ssh(cinfo)
                    errors.extend(child_errors)
                    warnings.extend(child_warnings)
                else:
                    warnmsg = "Unknown credential category=%s. info=%r" % (category, cinfo)
                    warnings.append(warnmsg)
            else:
                errmsg = "Credential info has no category. info=%r" % cinfo
                errors.append(errmsg)

        return errors, warnings

    def _validate_credential_basic(self, cred):
        """
            Validates the non-common fields of a 'basic' credential.
        """
        errors = []
        warnings = []

        if "username" in cred:
            if len(cred["username"].strip()) == 0:
                errmsg = "The 'username' for a basic credential cannot be empty."
                errors.append(errmsg)
        else:
            errmsg = "Basic credentials must have a 'username' field."
            errors.append(errmsg)

        if "password" not in cred:
            errmsg = "Basic credentials must have a 'password' field."
            errors.append(errmsg)

        return errors, warnings

    def _validate_credential_ssh(self, cred):
        """
            Validates the non-common fields of an 'ssh' credential.
        """
        """
        -   "identifier": "some-node"
            "category": "ssh"
            "username": "ubuntu"
            "password": "blahblah"
            "keyfile": "~/.ssh/id_somenode_rsa"

        """
        errors = []
        warnings = []

        if "username" in cred:
            if len(cred["username"].strip()) == 0:
                errmsg = "The 'username' for an SSH credential cannot be empty."
                errors.append(errmsg)
        else:
            errmsg = "SSH credentials must have a 'username' field."
            errors.append(errmsg)

        if "password" not in cred and "keyfile" not in cred:
            errmsg = "SSH credentials must have a 'password' or 'keyfile' field."
            errors.append(errmsg)
        elif "keyfile" in cred:
            keyfile = os.path.abspath(os.path.expanduser(os.path.expandvars(cred["keyfile"])))
            if not os.path.exists(keyfile):
                errmsg = "The specified SSH keyfile does not exist. file=%s" % keyfile
                errors.append(errmsg)

        return errors, warnings
