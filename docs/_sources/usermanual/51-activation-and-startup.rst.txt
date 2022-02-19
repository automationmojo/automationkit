.. _51-activation-and-startup:

**********************
Activation and Startup
**********************

The *Automation Kit* is designed to be used as a base for multiple types of automation
projects.  It can be used as a basis for interactive shells, commandline utilities, REST
services and testing frameworks.  Each of these types of projects have thier own characteristics
and behaviors with regard to logging, terminal output, database connectivity and possibly
others.  The *Automation Kit* provides different methods of activation that can be utilized
in order to ensure the correct behaviors are setup for each of these types of projects.  The
following is a list of activation and startup modes that are supported.

Workflow and Testing Runs
=========================

```python
import akit.environment.activate
```


Command or Script
=================

```python
import akit.environment.command
```


Interactive Console
===================

```python
import akit.environment.console
```


Service
=======

```python
import akit.environment.service
```

