.. _35-user-file:

****************
User File
****************


Location
========
The default location where the **Automation Kit** will look for the *user.yaml* file
is:

.. code-block:: text

    ~/akit/config/user.yaml


Description
===========

.. code-block:: yaml

    version: 1.0.0
    debugging:
      timemachine:
        active-portals: {}
    logging:
      branched:
      - loglevel: DEBUG
        logname: paramiko.transport.log
        name: paramiko.transport
      levels:
        console: INFO
        logfile: DEBUG
      logname: '%(jobtype)s.log'
