.. _34-credentials-file:

****************
Credentials File
****************


Location
========
The default location where the **Automation Kit** will look for the *credentials.yaml* file
is:

.. code-block:: text

    ~/akit/config/credentials.yaml


Environment Variable
====================
You can specify a different location and name for the *credentials.yaml* by setting the
*AKIT_CREDENTIALS* environment variable like so:

.. code-block:: bash

    AKIT_CREDENTIALS="/home/jenkins/workspace/credentials.yaml"

The **Automation Kit** does support expanding the *~* user and *$VARIABLE* environment
variables in the specific path.


Commandline Option
==================
The name and location of the *credentials.yaml* configuration file can also be specific
on the commandline.


Extensibility
=============


Description
===========

.. code-block:: yaml

    credentials:
        -   identifier: power
            category: basic
            username: ubuntu
            password: PowerPower**

        -   identifier: player-ssh
            category: ssh
            username: root
            password: BlahBlah!!
            primitive: True
