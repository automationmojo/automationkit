
import logging

from akit.exceptions import akit_assert
from akit.testing import testplus

def test_checkout_and_checkin_by_model(apod):
    """
        CRITICAL = 50
        FATAL = CRITICAL
        ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
    """
    testplus.logger.critical("This is an critical({}) message.".format(logging.CRITICAL))

    testplus.logger.error("This is an error({}) message.".format(logging.ERROR))

    testplus.logger.warn("This is a warning({}) message.".format(logging.WARN))

    testplus.logger.info("This is a info({}) message.".format(logging.INFO))

    testplus.logger.debug("This is a debug({}) message.".format(logging.DEBUG))

    return