

# pylint: disable=unused-import
# pylint: disable=cyclic-import

from datetime import datetime
import time

import akit.environment.activate

from akit.xlogging.foundations import logging_initialize

from akit.integration.landscaping.landscape import Landscape, startup_landscape

def coordinator_example_main():

    logging_initialize()

    lscape: Landscape = startup_landscape(include_upnp=True)

    s11 = lscape.checkout_a_device_by_modelNumber("S11").upnp

    svc_avt = s11.serviceAVTransport()

    var_cur_uri = svc_avt.lookup_default_variable("AVTransportURI")

    cur_uri = var_cur_uri.value

    print("")
    print("")
    print("Bdee bdee bdee, Thats all folks!")
    print("")
    print("")


if __name__ == "__main__":
    coordinator_example_main()
