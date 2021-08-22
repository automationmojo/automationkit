
import sys

from akit.exceptions import swap_error_for_akit_error

def raises_timeout():
    raise EOFError("Blah timed out.")

def intermediate_function():
    try:
        raises_timeout()
    except Exception as toerr:
        if hasattr(toerr, "kwargs"):
            print("Has kwargs")
        einst = swap_error_for_akit_error(toerr)
        raise einst from toerr


def main_exception_swap():
    try:
        intermediate_function()
    except Exception as toerr:
        print("Exception caught.")
    return





if __name__ == "__main__":
    main_exception_swap()