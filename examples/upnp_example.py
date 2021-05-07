

# pylint: disable=unused-import
# pylint: disable=cyclic-import

import time

import akit.environment.activate

from akit.xlogging.foundations import logging_initialize

from akit.integration.landscaping.landscape import Landscape

def coordinator_example_main():

    logging_initialize()

    lscape = Landscape()
    lscape.first_contact()

    s17 = lscape.checkout_a_device_by_modelNumber("S17")

    value = s17.action_GetLEDState()

    if s17.subscribe_to_events():
        var_zonename = s17.lookup_event_variable("ZoneName")
        znval = var_zonename.wait_for_value(timeout=600)
        print (var_zonename)

        isbval = s17.lookup_event_variable("IsZoneBridge")
        print (isbval)

    LEDSTATES = ["Off", "On"]

    SMALL_COUNTER = 0
    LARGE_COUNTER = 0
    while True:
        time.sleep(2)
        if SMALL_COUNTER == 0:
            print("tick")
        else:
            print("tock")

        if LARGE_COUNTER == 0:
            print("Refreshing upnp device status.")

        SMALL_COUNTER = (SMALL_COUNTER + 1) % 2
        LARGE_COUNTER = (LARGE_COUNTER + 1) % 30


if __name__ == "__main__":
    coordinator_example_main()
