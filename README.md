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

# Table of Contents
1. [Automation Software Stack](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/10-automation-software-stack.md)
2. [Getting Started](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/20-getting-started.md)
3. [Automation Configuration](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/30-automation-configuration.md)
    1. [Landscape File](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/31-landscape-file.md)
    2. [Topology File](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/32-topology-file.md)
    2. [Runtime File](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/33-runtime-file.md)
    3. [Credentials File](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/34-credentials-file.md)
4. [TestRun Sequencing](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/40-testrun-sequencing.md)
    1. [Integration Couplings](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/41-integration-couplings.md)
    2. [Scope Couplings](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/42-scope-couplings.md)
5. [Functional Description](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/50-functional-description.md)
    1. [Activation and Startup](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/51-activation-and-startup.md)
    2. [Inter-Operability](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/52-inter-operability.md)
    3. [SSH Coordinator and Agent](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/53-ssh-coordinator-and-agent.md)
    4. [UPNP Coordinator and Agent](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/54-upnp-coordinator-and-agent.md)
6. [Workflow Orchestration](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/60-workflow-orchestration.md)
7. [Enterprise Extensibility](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/70-enterprise-extensibility.md)
8. [Command Line](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/80-command-line.md)
9. [Code Organization and Conventions](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/90-code-organization-and-conventions.md)
10. [Coding Standards](https://github.com/automationmojo/automationkit/blob/main/docs/markdown/100-coding-standards.md)
