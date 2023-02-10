
from typing import Any, Callable, Dict, List

import inspect


from akit.exceptions import AKitSemanticError, AKitNotImplementedError


def mark_categories(*, categories: List[str]):
    """
        Used to mark a test with category markers.
    """

    def decorator(testfunc: Callable) -> Callable:

        if not hasattr(testfunc, "_metadata_"):
            testfunc._metadata_ = {}

            testfunc._metadata_["categories"] = categories

        return testfunc

    return decorator

def mark_keywords(*, keywords: List[str]):
    """
        Used to mark a test with a list of keywords.
    """

    def decorator(testfunc: Callable) -> Callable:

        if not hasattr(testfunc, "_metadata_"):
            testfunc._metadata_ = {}

            testfunc._metadata_["keywords"] = keywords

        return testfunc

    return decorator


def mark_priority(*, priority: int):
    """
        Used to mark a test with a priority.
    """

    def decorator(testfunc: Callable) -> Callable:

        if not hasattr(testfunc, "_metadata_"):
            testfunc._metadata_ = {}

            testfunc._metadata_["priority"] = str(priority)

        return testfunc

    return decorator


def mark_descendent_categories(*, categories: List[str]):
    """
        Used to mark a module and all tests that reside under it in scope with a list of categories.

        :param categories: A list of categories to assign to descendent groups and tests
    """
    
    caller_frame = inspect.stack()[1]
    calling_module = inspect.getmodule(caller_frame[0])

    if not hasattr(calling_module, "_metadata_"):
        calling_module._metadata_ = {}

    calling_module._metadata_["categories"] = categories

    return


def mark_descendent_keywords(*, keywords: List[str]):
    """
        Used to mark a module and all tests that reside under it in scope with a list of keywords.

        :param keywords: A list of keywords to assign to descendent groups and tests
    """
    
    caller_frame = inspect.stack()[1]
    calling_module = inspect.getmodule(caller_frame[0])

    if not hasattr(calling_module, "_metadata_"):
        calling_module._metadata_ = {}

    calling_module._metadata_["keywords"] = keywords

    return


def mark_descendent_priority(*, priority: int):
    """
        Used to mark a module and all tests that reside under it in scope with a priority.

        :param priority: A priority to assign te descendent groups and tests.
    """

    caller_frame = inspect.stack()[1]
    calling_module = inspect.getmodule(caller_frame[0])

    if not hasattr(calling_module, "_metadata_"):
        calling_module._metadata_ = {}

    calling_module._metadata_["priority"] = str(priority)

    return


class MetaFilter:

    def __init__(self, include: bool, group: str):
        self._include = include
        self._group = group
        return

    @property
    def group(self):
        return self._group

    @property
    def include(self):
        return self._include

    def should_include(self, metadata: Dict[str, Any]) -> bool:
        errmsg = "MetaFilter.should_include must be implemented in derived classes."
        raise AKitNotImplementedError(errmsg)


class MetaFilterContains(MetaFilter):

    def __init__(self, include: bool, group: str, value:str):
        super().__init__(include, group)
        self._value = value
        return
    
    def should_include(self, metadata: Dict[str, Any]) -> bool:

        include = False

        if metadata is not None:
            if self._group in metadata:
                found_marker = metadata[self._group]
                if isinstance(found_marker, str):
                    if found_marker.find(self._value) > -1:
                        include = True
                elif isinstance(found_marker, list) or isinstance(found_marker, tuple):
                    if self._value in found_marker:
                        include = True

        # If this is an exclude based match, then negate the logic
        # of the match
        if not self._include:
            include = False if include else True

        return include

class MetaFilterEquals(MetaFilter):

    def __init__(self, include: bool, group: str, value:str):
        super().__init__(include, group)
        self._value = value
        return

    def should_include(self, metadata: Dict[str, Any]) -> bool:

        include = False

        if metadata is not None:
            if self._group in metadata:
                found_marker = metadata[self._group]
                if found_marker == self._value:
                    include = True

        # If this is an exclude based match, then negate the logic
        # of the match
        if not self._include:
            include = False if include else True

        return include

class MetaFilterNotEquals(MetaFilterEquals):

    def __init__(self, include: bool, group: str, value:str):
        super().__init__(include, group, value)
        return

    def should_include(self, metadata: Dict[str, Any]) -> bool:

        include = super().should_include(metadata)
        include = False if include else True

        return include


def parse_marker_expression(expression: str):

    include = True
    group = None
    marker = None

    working_expr = expression.strip()

    include_symbol = working_expr[0]
    if include_symbol == "+":
        include = True
    elif include_symbol == "-":
        include = False
    else:
        errmsg = "Marker expressions must begin with a + (include) or - (exclude) symbol. expression={}".format(expression)
        raise AKitSemanticError(errmsg)

    # Strip off the include or exclude
    working_expr = working_expr[1:].lstrip()

    errmsg = "Marker expressions must be in the form (+ or -)(group)/(marker)(= or ~)(value). expression={}".format(expression)

    operator = None
    # Equals
    if working_expr.find("==") > 0:
        operator = "=="
        working_expr.split(operator)
    # Contains
    elif working_expr.find("~=") > 0:
        operator = "~="
    # Not Equal
    elif working_expr.find("!=") > 0:
        operator = "!="
    else:
        raise AKitSemanticError(errmsg)

    marker_group = None
    marker_value = None

    next_parts = working_expr.split(operator)
    if len(next_parts) == 1:
        if operator in ["==", "~=", "!="]:
            errmsg = 'Expressions using the "==", "~=", "!=" operators must have a value component. expression={}'.format(expression)
            raise AKitSemanticError(errmsg)
        marker_group = next_parts[0]
    elif len(next_parts) == 2:
        marker_group, marker_value = next_parts
    else:
        raise AKitSemanticError(errmsg)

    if operator == "==":
        metafilter = MetaFilterEquals(include, marker_group, marker_value)
    elif operator == "~=":
        metafilter = MetaFilterContains(include, marker_group, marker_value)
    elif operator == "!=":
        metafilter = MetaFilterNotEquals(include, marker_group, marker_value)
    else:
        errmsg = "Uh Oh. Did someone partially implement a new operator. expression={}".format(expression)
        raise AKitSemanticError(errmsg)

    return metafilter