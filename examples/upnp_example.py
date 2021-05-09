

# pylint: disable=unused-import
# pylint: disable=cyclic-import

import time

import akit.environment.activate

from akit.xlogging.foundations import logging_initialize

from akit.integration.landscaping.landscape import Landscape
from akit.mixins.upnpcoordinatormixin import UpnpCoordinatorMixIn

def coordinator_example_main():

    logging_initialize()

    # Initialize the Landscape
    lscape = Landscape()

    # Give the UpnpCoordinatorMixIn an opportunity to register itself
    UpnpCoordinatorMixIn.attach_to_framework(lscape)

    # Finalize the registration process and transition the landscape
    # to the activation phase
    lscape.registration_finalize()

    # Give the UpnpCoordinatorMixIn an opportunity to attache to its
    # environment and determine if the resources requested and the
    # resource configuration match
    UpnpCoordinatorMixIn.attach_to_environment()

    # Finalize the activation process and transition the landscape
    # to fully active where all APIs are available.
    lscape.activation_finalize()

    # Make initial contact with all of the devices
    lscape.first_contact()

    s18 = lscape.checkout_a_device_by_modelNumber("S18").upnp

    value = s18.getLedState()

    if s18.serviceDeviceProperties().subscribe_to_events():
        var_zonename = s18.serviceDeviceProperties().lookup_event_variable("ZoneName")
        znval = var_zonename.wait_for_value(timeout=600)
        print (var_zonename)

        isbval = s18.serviceDeviceProperties().lookup_event_variable("IsZoneBridge")
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
