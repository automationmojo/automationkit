.. _33-runtime-file:

************
Runtime File
************

Location
========
The default location where the **Automation Kit** will look for the *runtime.yaml* file
is:

.. code-block:: text

    ~/akit/config/runtimes/default-runtime.yaml

Environment Variable
====================
You can specify a different location and name for the *runtime.yaml* by setting the
*AKIT_RUNTIME* environment variable like so:

.. code-block:: bash

    AKIT_RUNTIME="/home/jenkins/workspace/runtime.yaml"

The **Automation Kit** does support expanding the *~* user and *$VARIABLE* environment
variables in the specific path.


Commandline Option
==================
The name and location of the *runtime.yaml* configuration file can also be specific
on the commandline.


Extensibility
=============
The runtime configuration is not designed to be extensible like the other configuration objects.
This is because the runtime configuration is stored as a big dictionary in the a global context.
The configuration is stored in this way so it can be easily serialized and passed, along with
the other context dictionary information, from the main automaiton process to any remote service
processes that might be deployed to remote devices as part of the automation *Establish Presence*
phase. This allows for the propagation of automation configuration across the entire test landscape
during the startup process.

Description
===========

.. code-block:: yaml

    diagnostics:
        archive:
            - /opt/log/anacapa.trace
            - /opt/log/netstartd.log
            - /opt/log/ssdpd.log
            - /opt/log/udhcpc.log

    upnp:
        exclude_interfaces:
            - lo
            - docker0
            - vpn0
            - br-16b3341898b9
        subscriptions:
            logged-events:
                # Un-Comment to turn on UPNP Event logging
                #"urn:schemas-upnp-org:service:DeviceProperties:1":
                    #- SettingsReplicationState