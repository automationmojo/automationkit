"""
.. module:: context
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`Context` object and :class:`ContextCursor` that
               are used to maintain the shared automation context.

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

from typing import Any, List, Optional

import re

from collections import ChainMap

from akit.environment.configuration import CONFIGURATION_MAP

REGEX_PATH_VALIDATOR = re.compile("/{1}([-a-zA-Z0-9_]+)")

def validate_path_name(path: str) -> List[str]:
    """
        Validates a context pathname.
    """
    parts = None
    mobj = REGEX_PATH_VALIDATOR.findall(path)
    if mobj is not None:
        parts = list(mobj)
    return parts

class ContextCursor:
    """
        The :class:`ContextCursor` serves as cursor into the storage dictionary that
        is used to store all the objects in the context.
    """
    def __init__(self, storeref: dict):
        self._storeref = storeref
        return

    @property
    def value(self):
        return self._storeref

    def fill_template(self, template: str) -> str:
        """
            Method that fills the provided template using the data items stored at the
            level of the context pointed to by this :class:`ContextCursor`
        """
        filled = template % self._storeref
        return filled

    def insert(self, path: str, obj: Any):
        """
            Insert an object at the path specified.

            :param path: Path where the object is to be inserted
            :param obj: The object to insert

            :raises: :class:`ValueError`
        """
        if isinstance(path, (tuple, list)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))

        self._insert(self._storeref, path, path_parts, obj)

        return

    def lookup(self, path: str, default: Optional[Any]=None) -> Any:
        """
            Lookup an object at the path specified.

            :param path: Path where the desired object is located.
            :param default: Optional default value that should be set and returned
                            if the lookup fails.

            :returns: The object stored at the specified path.

            :raises: :class:`LookupError`
        """
        found_node = None

        if isinstance(path, (tuple, list)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))

        found_node = self._lookup(self._storeref, path, path_parts, default=default)

        return found_node

    def remove(self, path: str, raise_error=False) -> Any:
        """
            Remove an object at the specified path

            :param path: Path where the desired object is located.

            :returns: The being removed from the specified path.

            :raises: :class:`LookupError`
        """
        found_node = None

        try:
            if isinstance(path, (tuple, list)):
                path_parts = path
                path = "/%s" %  "/".join(path_parts)
            else:
                path_parts = validate_path_name(path.rstrip("/"))

            found_node = self._remove(self._storeref, path, path_parts)
        except LookupError as luerr:
            if raise_error:
                raise

        return found_node

    def _insert(self, dref: dict, path: str, path_parts: List[str], obj: Any):

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if len(path_parts) > 1:
                if leaf_name not in dref:
                    dref[leaf_name] = {}
                found_node = dref[leaf_name]
                self._insert(found_node, path, path_parts[1:], obj)
            else:
                dref[leaf_name] = obj
        else:
            raise ValueError("Invalid path=%s" % path)

        return

    def _lookup(self, dref: dict, path: str, path_parts: List[str], default: Optional[Any]=None) -> Any:

        found_node = None

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in dref:
                found_node = dref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found_node, (dict, ChainMap)):
                        found_node = self._lookup(found_node, path, path_parts[1:], default=default)
                    else:
                        raise LookupError("Context lookup failure for path=%s" % path)
                else:
                    if isinstance(found_node, (dict, ChainMap)):
                        found_node = ContextCursor(found_node)
            elif default is not None:
                if len(path_parts) > 1:
                    found_node = {}
                    dref[leaf_name] = found_node
                    found_node = self._lookup(found_node, path, path_parts[1:], default=default)
                else:
                    dref[leaf_name] = default
                    found_node = default
            else:
                raise LookupError("Context lookup failure for path=%s" % path)
        else:
            raise ValueError("Invalid path=%s" % path)

        return found_node

    def _remove(self, dref: dict, path: str, path_parts: List[str]) -> Any:

        found_node = None

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in dref:
                found_node = dref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found_node, (dict, ChainMap)):
                        found_node = self._remove(found_node, path, path_parts[1:])
                    else:
                        raise LookupError("Context remove failure for path=%s" % path)
                else:
                    del dref[leaf_name]
            else:
                raise LookupError("Context remove failure for path=%s" % path)
        else:
            raise ValueError("Invalid path=%s" % path)

        return found_node

    def __contains__(self, key: str) -> bool:
        found = key in self._storeref
        return found

    def __getitem__(self, key: str) -> Any:
        found_node = self._lookup(self._storeref, key, [key])
        return found_node

    def __setitem__(self, key: str , val: Any):
        self._insert(self._storeref, key, [key], val)
        return

    def __repr__(self) -> str:
        return repr(self._storeref)

    def __str__(self) -> str:
        return str(self._storeref)

class Context:
    """
        The :class:`Context` object is a special dictionary derivative that utilizes a 'path'
        style syntax to store and retrieve values and objects.  The :class:`Context` also provides
        a storage facility that can be replicated or sharded across a distributed environment.
    """
    _instance = None
    _store: dict = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Context, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def insert(self, path: str, obj: Any):
        """
            Insert an object at the path specified.

            :param path: Path where the object is to be inserted
            :param obj: The object to insert

            :raises: :class:`ValueError`
        """
        if isinstance(path, (list, tuple)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))

        self._insert(self._store, path, path_parts, obj)

        return

    def lookup(self, path: str, raise_error=False, default: Optional[Any]=None) -> Any:
        """
            Lookup an object at the path specified.

            :param path: Path where the desired object is located.

            :returns: The object stored at the specified path.

            :raises: :class:`LookupError`
        """
        found_node = None

        try:
            if isinstance(path, (list, tuple)):
                path_parts = path
                path = "/%s" %  "/".join(path_parts)
            else:
                path_parts = validate_path_name(path.rstrip("/"))

            found_node = self._lookup(self._store, path, path_parts, default=default)
        except LookupError:
            if raise_error:
                raise

        return found_node

    def remove(self, path: str) -> Any:
        """
            Remove an object at the specified path

            :param path: Path where the desired object is located.

            :returns: The being removed from the specified path.

            :raises: :class:`LookupError`
        """
        found_node = None

        if isinstance(path, (list, tuple)):
            path_parts = path
            path = "/%s" %  "/".join(path_parts)
        else:
            path_parts = validate_path_name(path.rstrip("/"))

        found_node = self._remove(self._store, path, path_parts)

        return found_node

    def _insert(self, dref: dict, path: str, path_parts: List[str], obj: Any) -> Any:

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if len(path_parts) > 1:
                if leaf_name not in dref:
                    dref[leaf_name] = {}
                found_node = dref[leaf_name]
                self._insert(found_node, path, path_parts[1:], obj)
            else:
                dref[leaf_name] = obj
        else:
            raise ValueError("Invalid path=%s" % path)

        return

    def _lookup(self, dref: dict, path: str, path_parts: List[str], default: Optional[Any]=None) -> Any:

        found_node = None

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in dref:
                found_node = dref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found_node, (dict, ChainMap)):
                        found_node = self._lookup(found_node, path, path_parts[1:], default=default)
                    else:
                        raise LookupError("Context lookup failure for path=%s" % path)
                else:
                    if isinstance(found_node, (dict, ChainMap)):
                        found_node = ContextCursor(found_node)
            elif default is not None:
                if len(path_parts) > 1:
                    found_node = {}
                    dref[leaf_name] = found_node
                    found_node = self._lookup(found_node, path, path_parts[1:], default=default)
                else:
                    dref[leaf_name] = default
                    found_node = default
            else:
                raise LookupError("Context lookup failure for path=%s" % path)
        else:
            raise ValueError("Invalid path=%s" % path)

        return found_node

    def _remove(self, dref: dict, path: str, path_parts: List[str]) -> Any:

        found_node = None

        if len(path_parts) > 0:
            leaf_name = path_parts[0]
            if leaf_name in dref:
                found_node = dref[leaf_name]
                if len(path_parts) > 1:
                    if isinstance(found_node, (dict, ChainMap)):
                        found_node = self._remove(found_node, path, path_parts[1:])
                    else:
                        raise LookupError("Context remove failure for path=%s" % path)
                else:
                    del dref[leaf_name]
            else:
                raise LookupError("Context remove failure for path=%s" % path)
        else:
            raise ValueError("Invalid path=%s" % path)

        return found_node

    def __contains__(self, key: str) -> bool:
        found = key in self._store
        return found

    def __getitem__(self, key: str) -> Any:
        found_node = self._lookup(self._store, key, [key])
        return found_node

    def __setitem__(self, key: str, val: Any):
        self._insert(self._store, key, [key], val)
        return



# Initialize the global context

context = Context()
context.insert("/configuration", CONFIGURATION_MAP)
context.insert("/environment", {})

class ContextUser:
    """
        Serves as a base class for all classes that need a reference to the singleton context object.
    """
    context: Context = Context()
