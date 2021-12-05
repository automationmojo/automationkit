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
settings for the activation mode that is being used.  Activation modes are discussed in the
`Activation and Startup <https://github.com/automationmojo/automationkit/blob/main/docs/markdown/51-activation-and-startup.md>`_
section of the documentation.


Default Configuration
=====================

Environment Variables
=====================

Runtime Configuration
=====================

Commandline Options
===================
