

# pylint: disable=unused-import
# pylint: disable=cyclic-import

from datetime import datetime
import time

import akit.environment.activate

from akit.xlogging.foundations import logging_initialize

from akit.integration.landscaping.landscape import Landscape
from akit.mixins.upnpcoordinatorintegration import UpnpCoordinatorIntegration

def coordinator_example_main():

    logging_initialize()

    # ==================== Landscape Initialization =====================
    # The first stage of standing up the test landscape is to create and
    # initialize the Landscape object.  If more than one thread calls the
    # constructor of the Landscape, object, the other thread will block
    # until the first called has initialized the Landscape and released
    # the gate blocking other callers.
    lscape = Landscape()

    # Give the UpnpCoordinatorIntegration an opportunity to register itself, we are
    # doing this in this way to simulate test framework startup.
    UpnpCoordinatorIntegration.attach_to_framework(lscape)

    # Finalize the registration process and transition the landscape
    # to the activation phase
    lscape.registration_finalize()

    # Give the UpnpCoordinatorIntegration an opportunity to attach to its
    # environment and determine if the resources requested and the
    # resource configuration match
    UpnpCoordinatorIntegration.attach_to_environment()

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

        value, updated, changed, state = isbval.sync_read()

        print ("value={}, updated={} changed={} state={}".format(value, updated, changed, state.name))
        print ()

    var_zonename = s18.serviceDeviceProperties().lookup_event_variable("ZoneName")

    before_change = datetime.now()
    s18.setZoneName("Blah")
    znval = var_zonename.wait_for_update(before_change, timeout=600)

    print("")
    print("")
    print("Bdee bdee bdee, Thats all folks!")
    print("")
    print("")


if __name__ == "__main__":
    coordinator_example_main()
