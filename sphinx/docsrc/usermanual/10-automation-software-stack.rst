******************************
Test Automation Software Stack
******************************

The **Automation Kit** is meant to serve as a foundation of a distributed and scalable
automation software stack.  The diagram below and the descriptions in this section
describe the automation software stack that the **Automation Kit** is meant to be a part of.

.. image:: /_static/images/testing-software-stack.jpg
  :width: 400
  :alt: Test Automation Software Stack

The four layer software stack that is shown in the diagram helps to break down the
test automation stack into major groups which serves to establish good patterns and
practices for maintaining the software stack.  The patterns span different disciplines
of the software development process.

The **Automation Kit** servers as the core layer in the above software stack.  It
provides the foundation components on which to build a distributed automation software
stack and provides extensibility to make it easy to stack on a continuous integration
layer (core layer) and product layer which are aligned to the customized needs of Individual
enterprise consumers.  The core and product layers provide the customizations that implement
automation scenario variaces that are unique to a given enterprise.  This makes it easier
to use the **Automation Kit** as the foundation for any distributed automation project.

Product Alignment
=================
The software stack divides the source code up by product alignment.  This seperation of
product alignment means that source code can more easily be partitioned for deployment
in the enterprise.  The core and product components of the software stack that are
not closely aligned with the product under test, can be stored in repositories and
deployed based on repository style deployment techniques.

.. image:: /_static/images/testing-software-stack-alignment.jpg
  :width: 400
  :alt: Product Alignment

From the diagram you can see that the product and test code are the most closely
aligned to the product code and can be kept in the source tree with the product
code.  This means that changes to features and assocatied tests can be versioned
utilizing a parallel versioning scheme much like the feature specific product code
that is most often being versioned in parallel across multiple branches in a source
code repository.

### Risk, Impact and Testing Scope ###
The software stack also divides up the code by Risk and Impact.  Because the core and
product code are a central dependency for the test code.  They have a
higher risk when it comes to code changes.  They also are shared and so have higher
impact.

.. image:: /_static/images/testing-software-stack-impact.jpg
  :width: 400
  :alt: Risk and Impact

The fact that we seperate out the higher impact code into different layers, means that
we can establish risk appropriate patterns and practices that are followed when working with
the code at the given layers in the stack.  This is important as it allows us to align
the level of effort and resource expendature with the impact of the code that is being
modified.  We can make the product code easier for testers and individual contributors to
work in while still maintaining high levels of quality in the high impact code.  We can
also put special layer appropriate testing proceedures in place for the code at the core
and intergation layers.

.. image:: /_static/images/testing-software-stack-testscopes.jpg
  :width: 400
  :alt: Testing Scope

The diagram above shows how we can establish appropriate testing patterns and practices
for the code being merged into each level of the software stack.

Distributed Integration Model
=============================

The **AutomationKit** defines an object model that helps to create a test landscape
where automation activies can be conducted and coordinated.  The pre-defined object
model helps to eliminate a lot of experimental or trial and error activities when
standing up new automation products, by defining patterns that have been previously
utilized to successfully create large scale automation projects.

The **AutomationKit** is designed to be a good solid foundation which organizations
engaging in large scale automation projects can easily extend.  Organizations that
intend to utilize the **AutomationKit** would extend the base object model by building
a core layer and product layer that sit on top of the **AutomationKit** layer as depicted
in the diagram below.

.. image:: /_static/images/organization-test-software-stack.jpg
  :width: 400
  :alt: Test Automation Software Stack

The layout of the software stack shown above is critically important for creating a
robust automation stack that is easy to maintain at scale.  It is partitioned in such
a way as to hit a sweet spot between the needs of the Continuous Integration team and
the Individual Test Contributors on many levels.

Lets look at the different partitioning levels.


AutomationKit (akit)
--------------------
* environment Activation /Startup (console/scripts/service)
* Logging
* Well Known Protocols (ssh/upnp)
* Networking
* Formatting
* Test Framework
* Configuration Management
* Foundation Landscape Management

Core Layer
----------
* Code that interoperate with the continuous integration environment
* Code that is hard to test with unit tests because it needs enterprise specific configuration
  or that interacts with external resources such as devices or services
* Product related code that can be updated independant of a branches
* Product related code that talks to a fixed interface and ca be versioned independant of product
  branch or product changes
* Product related interop code that changes very infrequently (contract interfaces)
* Product related code not related to a feature and generally not owned by a single team that
  is not likely to change often

Product Layer
-------------
* Product code that is likely to be shared across teams and is likely to undergo
  frequent change and is versioned in parallel across branches during periods of change
* Product related code that is related to a feature (playback, grouping, alarms, room detection)
* Test helper code and fixtures that are shared across tests and teams
* Any code that relates to the product that is not a testcase implementation

Test Layer
----------
* Product testcase code


Extensibility
=============

The sections below describe the integration model that is utilized by the **AutomationKit**
in order to quickly stand up robust automation projects.

Landscape
---------

The **AutomationKit** utilizes the concept of the "Test Landscape" in order to provide
a means of organizing, coordinating activities with and monitoring resources associated
with an automation run.  The "Test Landscape" is an abstraction that represents all of
the intergrated resources that are available and or required for an automation run. The
test framework and tests utilize an instance of the **Landscape** object in order to
interact with external resources that are to be integrated into an automation run.

The **Landscape** object loads a description of the landscape from a 'yaml' file located
at '~/akit/config/landscape.yaml' or from the file specified by a command-line parameter
or via the 'AKIT_LANDSCAPE' environment variable.  A description of the landscape file
format and properties is described in the `landscape description documentation<https://github.com/automationmojo/automationkit/blob/main/docs/markdown/31-landscape-file.md>`.

The **Landscape** object utilizes Coordinator objects to manage external automation
resources such as devices, serial connections, and power connections.  The coordinators
are loaded based on whether or not a test or other framework consumer includes a
coordinator or device integration fixture which indicates that resources are required
for automation.  Once the test framework finds an integration fixture, it commences the
process of querying the fixture for information about the test resources that will be
required or utilized by the test run and provides the fixtures with an opportunity to
integrate any required resources.

.. image:: /_static/images/akit-integration-model.jpg
  :width: 400
  :alt: Integration Object Model

.. note::
    The **Landscape** object can be extended by organizations in order to integrate
    custom landscape descriptions, device coordinators, devices and other resources
    into the test landscape for the organization.
