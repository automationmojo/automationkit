******************************
Test Automation Software Stack
******************************

    *in-progress*


Automation Software Stack
=========================

The **Automation Kit** is meant to serve as a foundation of an automation software
stack.  The diagram below and the descriptions in this section describe the automation
software stack that the **Automation Kit** is meant to be a part of.

.. image:: /_static/images/testing-software-stack.jpg
  :width: 600
  :alt: Test Automation Software Stack

The four layer software stack that is shown in the diagram helps to break down the
test automation stack into major groups which serves to establish good patterns and
practices for maintaining the software stack.  The patterns span different disciplines
of the software development process such as:

* Testing Changes
* Integrated Testing of Changes
* Code Review Restrictions
* Versioning and Deploying Changes

The **Automation Kit** servers as the foundation layer in the above software stack.  It
provides the components on which to build a distributed automation software stack and
provides extensibility to make it easy to adapt the foundation layer to different automation
scenarios and to build core and integration layers as dependent packages.  This makes it
easier to use the **Automation Kit** as the foundation for any distributed automation project
and itegrate to it into an enterprise continuous integration system.

Product Alignment
-----------------
The software stack divides the source code up by product alignment.  This seperation of
product alignment means that source code can more easily be partitioned for deployment
in the enterprise.  The **Automation Kit** and core components of the software stack that
are not closely aligned with the product under test, can be stored in repositories and
deployed based on repository style deployment techniques.

.. image:: /_static/images/testing-software-stack-alignment.jpg
  :width: 600
  :alt: Product Alignment

From the diagram you can see that the product layer and test code layer are the most
closely aligned to the the product code and can be kept in the source tree with the
product code.  This means that changes to features and assocatied tests can be versioned
in the branch along with the feature code.

### Risk, Impact and Testing Scope ###
The software stack also divides up the code by **Risk and Impact**.  Because the 
**Automation Kit** and core layer code is a central dependency for the product layer and
test code layer.  They have a higher risk when it comes to code changes.  They also are
shared and so have higher impact.

.. image:: /_static/images/testing-software-stack-impact.jpg
  :width: 600
  :alt: Risk and Impact

The fact that we seperate out the higher impact code into different layers, means that
we can establish different patterns and practices that are followed with working with
the code at the given layers in the stack.  This is important as it allows us to make
the process of making changes to lower impact product code easier for testers but still
maintaining stricter processes and higher quality in the high impact code.  We can also
put special layer appropriate testing proceedures in place for the code at the core and
intergation layers.

.. image:: /_static/images/testing-software-stack-testscopes.jpg
  :width: 600
  :alt: Testing Scope

The diagram above shows how we can establish appropriate testing patterns and practices
for the code being merged into each level of the software stack.

Distributed Integration Model
-----------------------------

The **Automation Kit** defines an object model that helps to create a test landscape
where automation activies can be conducted and coordinated.  The pre-defined object
model helps to eliminate a lot of experimental or trial and error activities when
standing up new automation products, by defining patterns that have been previously
utilized to successfully create large scale automation projects.

The **Automation Kit** is designed to be a good solid foundation which organizations
engaging in large scale automation projects can easily extend.  Organizations that
intend to utilize the **Automation Kit** would extend the base object model by building
an integration layer and product layer that sits on top of the **Automation Kit** layer
as depicted in the diagram below.

.. image:: /_static/images/organization-test-software-stack.jpg
  :width: 600
  :alt: Test Automation Software Stack

The layout of the software stack shown above is critically important for creating a
robust at scale.  It is partitioned in such a way as to hit a sweet spot between the
needs of the Continuous Integration team and the Individual Test Contributors on many
levels.  If you want to understand the importance of the partitioning shown you can
read an in depth explanation on the `Test Automation Software Stack - Details <https://github.com/automationmojo/automationkit/blob/main/docs/markdown/test-automation-software-stack-details.md>`_

The sections below describe the integration model that is utilized by the **Automation Kit**
in order to quickly stand up robust automation projects.

Landscape
---------

The **Automation Kit** utilizes the concept of the test **Landscape** in order to provide
a means of organizing, coordinating activities with and monitoring resources associated
with an automation run.  The **Landscape** is an abstraction that represents all of
the intergrated resources that are available and or required for an automation run. The
test framework and tests utilize an instance of the **Landscape** object in order to
interact with external resources that are to be integrated into an automation run.

The **Landscape** object loads a description of the landscape from a 'yaml' file located
at '~/akit/config/landscape.yaml' or from the file specified by a command-line parameter
or via the 'AKIT_LANDSCAPE' environment variable.  A description of the landscape file
format and properties is described in the `landscape description documentation <https://github.com/automationmojo/automationkit/blob/main/docs/markdown/31-landscape-file.md>`_.

The **Landscape** object utilizes Coordinator objects to manage external automation
resources such as devices, serial connections, and power connections.  The coordinators
are loaded based on whether or not a test or other framework consumer includes a
coordinator or device integration fixture which indicates that resources are required
for automation.  Once the test framework finds an integration fixture, it commences the
process of querying the fixture for information about the test resources that will be
required or utilized by the test run and provides the fixtures with an opportunity to
integrate any required resources.

.. image:: /_static/images/akit-integration-model.jpg
  :width: 600
  :alt: Integration Object Model

.. note::
    The **Landscape** object can be extended by organizations in order to integrate
    custom landscape descriptions, device coordinators, devices and other resources
    into the test landscape for the organization.
