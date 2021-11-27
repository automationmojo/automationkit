
from typing import List, Optional

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