
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import os

import click

from akit.environment.variables import LOG_LEVEL_NAMES

@click.group("upnp")
def group_generators_upnp():
    return

@click.command("generate")
def command_generators_upnp_generate():
    # We want to run the scan as a console application so we import the console
    # environment in order to setup the appropriate logging
    import akit.environment.console

    from akit.integration.upnp.generator.upnpgenerator import generate_service_proxies

    from akit.integration.upnp.paths import DIR_UPNP_GENERATOR_STANDARD_SERVICES
    from akit.integration.upnp.paths import DIR_UPNP_EXTENSIONS_STANDARD_SERVICES

    from akit.integration.upnp.paths import DIR_UPNP_SCAN_INTEGRATION_SERVICES
    from akit.integration.upnp.paths import DIR_UPNP_EXTENSIONS_INTEGRATION_SERVICES

    if os.path.exists(DIR_UPNP_GENERATOR_STANDARD_SERVICES):
        generate_service_proxies(DIR_UPNP_GENERATOR_STANDARD_SERVICES, DIR_UPNP_EXTENSIONS_STANDARD_SERVICES)

    if os.path.exists(DIR_UPNP_SCAN_INTEGRATION_SERVICES):
        generate_service_proxies(DIR_UPNP_SCAN_INTEGRATION_SERVICES, DIR_UPNP_EXTENSIONS_INTEGRATION_SERVICES)

    return

@click.command("scan")
def command_generators_upnp_scan():
    # We want to run the scan as a console application so we import the console
    # environment in order to setup the appropriate logging
    import akit.environment.console

    from akit.integration.landscaping.landscape import Landscape
    from akit.mixins.upnpcoordinatorintegration import UpnpCoordinatorIntegration

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
    lscape.transition_to_activation()

    # Give the UpnpCoordinatorIntegration an opportunity to attach to its
    # environment and determine if the resources requested and the
    # resource configuration match
    UpnpCoordinatorIntegration.attach_to_environment()

    # Finalize the activation process and transition the landscape
    # to fully active where all APIs are available.
    lscape.transition_to_operational(upnp_recording=True)

    # Make initial contact with all of the devices, this will trigger a scan
    # and the scan will populate the appropriate xml metadata directories
    UpnpCoordinatorIntegration.establish_presence()

    return

group_generators_upnp.add_command(command_generators_upnp_generate)
group_generators_upnp.add_command(command_generators_upnp_scan)
