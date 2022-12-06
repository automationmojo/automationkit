.. _30-automation-configuration:

************************
Automation Configuration
************************

The *Automation Kit* is designed to be intergated into an organizations continuous
integration system.  The automation kit can be configured by using environment variables,
commandline options, and through configuration files.  When the same option is configurable
via more than one of these mechanisms, the automation kit will prioritize the setting
based on precidence.  The precidence which the automation kit uses from lowest to highest
for settings is:

    * Default Configuration
    * Environment Variables
    * Runtime Configuration (file)
    * Commandline Option

So by default if nothing is passed for a setting, the *Automation Kit* will utilize default
settings for the activation mode that is being used.  Activation modes provide a quick way to
spin up various types of automation applications and services.  The activation modes supported are:

    * Command - Command line logging semantics
    * Console - Interactive console
    * Service - Web service and micro-services
    * TestRun - Test Automation run

The Activation modes are discussed in more detail in the
`Activation and Startup <https://github.com/automationmojo/automationkit/blob/main/docs/markdown/51-activation-and-startup.md>`_
section of the documentation.


Default Configuration
=====================
The default configuration for the *Automation Kit* provides easy setup for individual contributors to
help ensure the proficiency of the many individual contributors of the automation organization.  The
default configuration provides generic settings for automation framework behaviors and configuration file
locations.


Environment Variables
=====================

Build Information
-----------------
    AKIT_BUILD_BRANCH = The name of the branch to associate with results. Default is "unknown"
    AKIT_BUILD_FLAVOR = The label for the flavor of the build to associated with the results. Default is "unknown"
    AKIT_BUILD_NAME = The build name or build number to associate with the results."unknown"

Job Runtime Configuration
-------------------------
    AKIT_JOBTYPE = The type of run. "unknown"
    AKIT_RUNID = A guid that is used to uniquely identify and correlate the run results.
    AKIT_SERVICE_NAME = A service name used when the Automation Kit environment is activated as a service.
    AKIT_STARTTIME = The start time to use for correlating results.

    .. note: Job types supported are command, console, testrun, orchestration, service

Logging Configuration
---------------------
    AKIT_LOG_LEVEL_CONSOLE = The maximum logging level to send to the console output.
    AKIT_LOG_LEVEL_FILE = The maximum logging level to send to the primary log file.

    .. note: Logging levels supported are NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL, QUIET

Debug Options
-------------
    AKIT_BREAKPOINTS = A comma seperated list of wellknown breakpoints.
    AKIT_DEBUGGER = The name of a debug to activate on for the run.

    AKIT_TIMETRAVEL = Activates time travel debugging for the run.
    AKIT_TIMEPORTALS = A comman seperated list of wellknown time portals to activate for the run.

Files and Directories
---------------------
    AKIT_HOME_DIRECTORY = The base directory of the automation inputs and outputs "~/akit".
    AKIT_TESTROOT = The base directory of the test root folder.

    AKIT_CONFIG_DIRECTORY = The base directory for automation configuration "~/akit/config".
    AKIT_CONFIG_CREDENTIALS = The credential configuration file. "~/akit/config/credentials.yaml"
    
    AKIT_CONFIG_LANDSCAPE_NAME = The base name of the landscape configuration file. "default-landscape"
    AKIT_CONFIG_LANDSCAPE = The landscape configuration file. "~/akit/config/landscapes/{AKIT_CONFIG_LANDSCAPE_NAME}.yaml"
    
    AKIT_CONFIG_RUNTIME_NAME = The base name of the runtime configuration file. "default-runtime"
    AKIT_CONFIG_RUNTIME = The runtime configuration file. "~/akit/config/runtimes/{AKIT_CONFIG_RUNTIME_NAME}.yaml"
    
    AKIT_CONFIG_TOPOLOGY_NAME = The base name of the topology configuration file. "default-topology"
    AKIT_CONFIG_TOPOLOGY = The topology configuration file. "~/akit/config/topologies/{AKIT_CONFIG_TOPOLOGY_NAME}.yaml"
    
    AKIT_CONFIG_USER = The user configuration file. "~/akit/config/user.yaml"
    AKIT_OUTPUT_DIRECTORY = The ouput directory for results. The default depends on the type of run.

Landscape Overrides
-------------------
    AKIT_SKIP_DEVICES = The identifiers of devices that should be skipped.

Results Customization
---------------------
    AKIT_RESULTS_STATIC_RESOURCE_DEST_DIR = The destination for static resources files. "~/akit/results/static"
    AKIT_RESULTS_STATIC_RESOURCE_SRC_DIR = The folder of the source files for static resources. "{AKIT_DIR}/templates/static"
    AKIT_RESULTS_HTML_TEMPLATE = The file path of the HTML template file

Extensibility Customizations
----------------------------
    AKIT_CONFIG_LANDSCAPE_MODULE = The name of a module that contains a 'Landscape' override class.
    AKIT_UPNP_SCAN_INTEGRATION_BASE = The base directory for storing upnp code generator scan results.
    AKIT_UPNP_EXTENSIONS_INTEGRATION_BASE = The base directory for depositing code generated upnp device and service extensions.
    AKIT_UPNP_DYN_EXTENSIONS_MODULE = The base module name where code generated extions can be loaded from.

Configuration Files
===================

.. image:: /_static/images/automation-config.png
    :width: 400
    :alt: Automation Configuration Layout

Landscape File
--------------

:ref:`31-landscape-file`.

Topology File
-------------

:ref:`32-topology-file`.

Runtime File
------------

:ref:`33-runtime-file`.

Credential File
---------------

:ref:`34-credentials-file`.

User File
---------

:ref:`35-user-file`.

Commandline Options
===================
Command line options are available for specific commands which will override the variables and runtime
configuration options.