.. _32-topology-file:

*************
Topology File
*************

The **Automation Kit** currently does not have a fixed format for the topology
file. The topology file is intended for organizations to be able to configure
landscape resources to the specific unique project specific states that apply
to the uses of the devices and resources declared in the landscape.py file.


Location
========
The default location where the **Automation Kit** will look for the *topology.yaml* file
is:

.. code-block:: text

    ~/akit/config/topologies/default-topology.yaml


Environment Variable
====================
You can specify a different location and name for the *topology.yaml* by setting the
*AKIT_TOPOLOGY* environment variable like so:

.. code-block:: bash

    AKIT_TOPOLOGY="/home/jenkins/workspace/topology.yaml"

The **Automation Kit** does support expanding the *~* user and *$VARIABLE* environment
variables in the specific path.


Commandline Option
==================
The name and location of the *topology.yaml* configuration file can also be specific
on the commandline.


Extensibility
=============


Description
===========

Add a description that describes the details of your topology file content formatting here.


