# Automation Kit Repository

Welcome to the Automation Kit repository!


*Note:* This package is progressing quickly but is not yet ready for full production environments.

# Description
The **Automation Kit** is a python toolkit for building distributed automated task and testing systems.  It goes beyond the capabilities of other task and test automation frameworks by providing a hybrid approach that allows for dependency injection, similar to pytest, combined with and object oriented framework that can be utilized to easily customize the orchestration of tasks and tests across a collection of integrated resources.  Because the **Automation Kit** is built from the start with distributed automation in mind, it can help you quickly get distributed automated systems up and running that are based on a tested and proven set of object patterns and APIs.

# Design Philosophies
This section covers some of the important design features of the **Automation Kit** framework.

## Large Scale
The **Automation Kit** is designed for enterprise level distributed automation *"at scale"*.  The term *"at scale"* refers not only to a larger collection of enterprise resources but also refers to the fact that the **Automation Kit** helps to setup patterns that will support working in a very large code base.  The size of a code base that you might see associated with large enterprise level projects.  The **Automation Kit** supports working in large code bases by helping to establish good code organizational patterns and abstractions that support characteristics that:

* make it easier to learn and work in the code base
* make the code base easier to maintain
* make it easier to share and reuse code

## Faster Classification of Issues
One of the key philosophies behind the **Automation Kit** design is one of being able quickly and efficiently identify the nature of issues that come up during automation runs.  The **Automation Kit** initially classifies errors into one of four categories:

* **Configuration** - We identify configuration issues quickly and classify them so as to ensure that resources are not waisted troubleshooting configuration related issues and that eronious test results or noise is not generated due to configuration related issues. We also want automation runs to fail out quickly if the automation configuration is not setup correctly, before waisting additional testing resources.
* **Environment** - The **Automation Kit** performs an initial diagnostic scan of the automation landscape and all the resources declared to be necessary to run a series of tasks or tests in order to provide indications of environmental failures as early as possible.  This is important to ensure that we do not generate noise in automation results that are not related to the automation tasks or tests that might fail.  Just as with configuration, we want automation runs to fail out quickly if the automation environment is not setup correctly.
* **Error** - The **Automation Kit** classifies un-expected errors, or errors that are not founded in an expectation of a result, as an **Error** condition.  This helps to ensure these errors are given an appropriate initial direction or indication that the issues is a problem in the automation code and not an issue in the code that is the target of the automation run.
* **Failure** - The **AutomationKit** classifies failures that are associated with an expectation of behavior from a target under test as failures.  This allows for the proper initial classification of an issue as being a problem that is likely a failure in the code being targeted by the automation and the behavior or result it should have exhibited.

Having the initial classification of issues fall into one of these four categories helps to ensure that issues are easier to triage and assign to the appropriate party for investigation and resolution. It also helps to establish categories that can be used for data collection in order to better analyse the performance of test infrastructure, test code and product code.

## Integration and Distributed Automation Support
The **Automation Kit** comes with enterprise level integration and distributed automation capabilities.  The framework utilizes a customize-able set of classes that guides enterprise users through a process of creating a very robust integration object model based on the roles that enterprise resources play in an automation landscape.

The declaration of a custom automation landscape is as simple as setting an environment variable or passing a command line flag declaring the python module that contains a custom landscape derived class.  The *Landscape* and *LandscapeDescription* derived classes work together to provide the **Automation Kit** with a description of the customized roles and integration mixin(s) that provide the connection between the tasks and test automation code.

## Task and Test Integration Declaration and Assurance
The **Automation Kit** utilizes its object model to allow tasks and tests to provide information about their associated integration points and scopes of execution to the automation framework.  This integration declaration mechanism allows the automation framework to provide an early scan of the integration pathways and provide levels of assurance as to the stability of the automation landscape early in the automation process.  This is vitally important as it eliminates the waist and noise that are often associated with automation runs that are performed against an automation Landscape that has broken, mis-configured or missing resources.

## Automation Job, Scope and Flow Control 
The **Automation Kit** allows enterprise users to organize and customize the ordering of automation scope engagements and the flow of an automation job.  This provides the automation engineer the ability to control the engagement of automation scopes of execution and allows for optimal use of time and overlapping of scopes of execution in a test run.

## Automation Software Stack
The **Automation Kit** is meant to serve as a foundation of an automation software stack.  The diagram below and the descriptions in this section describe the automation software stack that the **Automation Kit** is meant to be a part of.

![Test Automation Software Stack](./images/testing-software-stack-deps.jpg?raw=true)

The four layer software stack that is shown in the diagram helps to break down the test automation stack into major groups which serves to establish good patterns and practices for maintaining the software stack.  The patterns span different disciplines of the software development process.

The **Automation Kit** servers as the core layer in the above software stack.  It provides the foundation components on which to build a distributed automation software stack and provides extensibility to make it easy to adapt the core layer to different automation scenarios and to build an integration layer on top of.  This makes it easier to use the **Automation Kit** as the foundation for any distributed automation project and itegrate it into an enterprise continuous integration system.

### Product Alignment ###
The software stack divides the source code up by product alignment.  This seperation of product alignment means that source code can more easily be partitioned for deployment in the enterprise.  The core and intergation components of the software stack that are not closely aligned with the product under test, can be stored in repositories and deployed based on repository style deployment techniques.

![Product Alignment](./images/testing-software-stack-alignment.jpg?raw=true)

From the diagram you can see that the mid-tier and test code are the most closely aligned to the the product code and can be kept in the source tree with the product code.  This means that changes to features and assocatied tests can be versioned in the branch along with the feature code.

### Risk, Impact and Testing Scope ###
The software stack also divides up the code by Risk and Impact.  Because the core and integration code is a central dependency for the mid-tier and test code.  They have a higher risk when it comes to code changes.  They also are shared and so have higher impact.

![Risk and Impact](./images/testing-software-stack-impact.jpg?raw=true)

The fact that we seperate out the higher impact code into different layers, means that we can establish different patterns and practices that are followed with working with the code at the given layers in the stack.  This is important as it allows us to make changes to lower impact product code easier for testers but still maintaining quality in the high impact code.  We can also put special layer appropriate testing proceedures in place for the code at the core and intergation layers.

![Testing Scope](./images/testing-software-stack-testscopes.jpg?raw=true)

The diagram above shows how we can establish appropriate testing patterns and practices for the code being merged into each level of the software stack.


### Distributed Integration Model ###
The **AutomationKit** defines an object model that helps to create a test landscape where automation activies can be conducted and coordinated.  The pre-defined object model helps to eliminate a lot of experimental or trial and error activities when standing up new automation products, by defining patterns that have been previously utilized to successfully create large scale automation projects.

The **AutomationKit** is designed to be a good solid foundation which organizations engaging in large scale automation projects can easily extend.  Organizations that intend to utilize the **AutomationKit** would extend the base object model by building an integration layer and product layer that sits on top of the **AutomationKit** layer as depicted in the diagram below.

![Test Automation Software Stack](./images/organization-test-software-stack.jpg?raw=true)

The layout of the software stack shown above is critically important for creating a robust at scale.  It is partitioned in such a way as to hit a sweet spot between the needs of the Continuous Integration team and the Individual Test Contributors on many levels.  If you want to understand the importance of the partitioning shown you can read an in depth explanation on the ![Test Automation Software Stack - Details](./docs/markdown/test-automation-software-stack-details.md)

The sections below describe the integration model that is utilized by the **AutomationKit** in order to quickly stand up robust automation projects.

#### Landscape ####
The **AutomationKit** utilizes the concept of the "Test Landscape" in order to provide a means of organizing, coordinating activities with and monitoring resources associated with an automation run.  The "Test Landscape" is an abstraction that represents all of the intergrated resources that are available and or required for an automation run. The test framework and tests utilize an instance of the **Landscape** object in order to interact with external resources that are to be integrated into an automation run.

The **Landscape** object loads a description of the landscape from a 'yaml' file located at '~/akit/config/landscape.yaml' or from the file specified by a command-line parameter or via the 'AKIT_LANDSCAPE' environment variable.  A description of the landscape file format and properties is described in the ![landscape description documentation](./docs/markdown/31-landscape-file.md).

The **Landscape** object utilizes Coordinator objects to manage external automation resources such as devices, serial connections, and power connections.  The coordinators are loaded based on whether or not a test or other framework consumer includes a coordinator or device integration fixture which indicates that resources are required for automation.  Once the test framework finds an integration fixture, it commences the process of querying the fixture for information about the test resources that will be required or utilized by the test run and provides the fixtures with an opportunity to integrate any required resources.

![Integration Object Model](./images/akit-integration-model.jpg?raw=true)

---
**NOTE:** The **Landscape** object can be extended by organizations in order to integrate custom landscape descriptions, device coordinators, devices and other resources into the test landscape for the organization.

---

# Table of Contents
1. [Automation Software Stack](./docs/markdown/10-automation-software-stack.md)
2. [Getting Started](./docs/markdown/20-getting-started.md)
3. [Automation Configuration](./docs/markdown/30-automation-configuration.md)
    1. [Landscape File](./docs/markdown/31-landscape-file.md)
    2. [Topology File](./docs/markdown/32-topology-file.md)
    2. [Runtime File](./docs/markdown/33-runtime-file.md)
    3. [Credentials File](./docs/markdown/34-credentials-file.md)
4. [TestRun Sequencing](./docs/markdown/40-testrun-sequencing.md)
    1. [Integration Couplings](./docs/markdown/41-integration-couplings.md)
    2. [Scope Couplings](./docs/markdown/42-scope-couplings.md)
5. [Inter-Operability](./docs/markdown/50-inter-operability.md)
    1. [SSH Coordinator and Agent](./docs/markdown/51-ssh-coordinator-and-agent.md)
    2. [UPNP Coordinator and Agent](./docs/markdown/52-upnp-coordinator-and-agent.md)
6. [Workflow Orchestration](./docs/markdown/60-workflow-orchestration.md)
7. [Enterprise Extensibility](./docs/markdown/70-enterprise-extensibility.md)
8. [Command Line](./docs/markdown/80-command-line.md)
9. [Code Organization and Conventions](./docs/markdown/90-code-organization-and-conventions.md)
10. [Coding Standards](./docs/markdown/100-coding-standards.md)
