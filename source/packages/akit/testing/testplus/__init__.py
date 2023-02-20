

from akit.xlogging.foundations import getAutomatonKitLogger

from akit.exceptions import akit_skip

from .markers import (
    mark_categories,
    mark_keywords,
    mark_priority,
    mark_descendent_categories,
    mark_descendent_keywords,
    mark_descendent_priority
)

from .parameters import (
    originate_parameter,
    param
)


from .resources import (
    integration,
    resource,
    scope
)

from .verification import (
    assert_dict_response_has_keys,
    assert_dict_response_has_paths,
    assert_equal,
    assert_expression,
    assert_greater,
    assert_lessthan,
    assert_list_length,
    assert_list_length_greater,
    assert_type
)

logger = getAutomatonKitLogger()

skip_test = akit_skip

__all__ = [
    assert_dict_response_has_keys,
    assert_dict_response_has_paths,
    assert_equal,
    assert_expression,
    assert_greater,
    assert_lessthan,
    assert_list_length,
    assert_list_length_greater,
    assert_type,
    integration,
    logger,
    mark_categories,
    mark_keywords,
    mark_priority,
    mark_descendent_categories,
    mark_descendent_keywords,
    mark_descendent_priority,
    originate_parameter,
    param,
    resource,
    scope,
    skip_test
]
