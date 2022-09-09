
from typing import Any, Iterable

def compare_any_of_same_type(expected: Any, found: Any) -> bool:
    result = None

    exp_type = type(expected)
    fnd_type = type(found)

    if exp_type != fnd_type:
        errmsg = "The types of the expected and found parameters be identical. exptype={} fndtype={}".format(exp_type, fnd_type)
        raise ValueError(errmsg)

    if exp_type == dict:
        compare_dict(expected, found)
    elif exp_type == list or exp_type == tuple:
        compare_iterables(expected, found)
    else:
        result = expected == found

    return result

def compare_dict(expected: dict, found: dict) -> bool:
    
    result = True

    if len(found) != len(expected):
        result = False

    else:
        for expkey, expval in expected.items():
            if expkey not in found:
                result = False
                break

            fndval = found[expkey]
            if type(expval) != type(fndval):
                result = False
                break

            result = compare_any_of_same_type(expval, fndval)
            if not result:
                break

    return result

def compare_iterables(expected: Iterable, found: Iterable) -> bool:

    result = True

    if len(found) != len(expected):
        result = False

    else:
        for eitem in expected:
            if eitem not in found:
                result = False
                break

    return result
