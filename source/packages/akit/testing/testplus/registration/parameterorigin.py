
from typing import Any, Callable, Dict, Optional, Type, Union

import inspect

from akit.testing.testplus.registration.sourcebase import SourceBase
from akit.testing.testplus.resourcelifespan import ResourceLifespan

class ParameterOrigin:

    def __init__(self, originating_scope: str, identifier: str, source: SourceBase, life_span: ResourceLifespan, constraints: Optional[Dict]):
        self._originating_scope = originating_scope
        self._identifier = identifier
        self._source = source
        self._life_span = life_span
        self._constraints = constraints
        return

    @property
    def constraints(self) -> Union[dict, None]:
        """
            Returns the most applicable constraints assoceated with this resource subscription.  If the
            subscription constraints are set then they will be used.  If the subscription constraints are
            not set and the source constraints are set, then the source constraints will be returned. If
            no constraints are applied to the subscription or the source, 'None' will be returned.
        """
        cval = None
        if self._constraints is not None:
            cval = self._constraints
        elif self._source.constraints is not None:
            cval = self._source.constraints
        return cval

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def life_span(self) -> ResourceLifespan:
        return self._life_span

    @property
    def originating_scope(self) -> str:
        return self._originating_scope

    @property
    def source_function(self) -> Callable:
        return self._source.source_function

    @property
    def source_function_name(self) -> str:
        return self._source.source_function.__name__

    @property
    def source_signature(self) -> inspect.Signature:
        return self._source.source_signature

    @property
    def source_id(self) -> str:
        idstr = self._source.source_id
        return idstr

    @property
    def source_module_name(self) -> str:
        return self._source.module_name

    @property
    def source_resource_type(self) -> Type:
        return self._source.resource_type

    def describe_source(self):
        descstr = self.source_id
        cval = self.constraints
        if cval is not None:
            descstr += " constraints={}".format(repr(cval))
        return descstr

    def generate_call(self):
        call_arg_str = ""
        call_args = [param for param in self.source_signature.parameters]
        if len(call_args) > 0:
            call_arg_str = ", ".join(call_args)
        call_str = "{}({})".format(self._source.source_function.__name__, call_arg_str)
        return call_str