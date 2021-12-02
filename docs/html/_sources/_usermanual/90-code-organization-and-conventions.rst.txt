*****************
Code Organization
*****************

    *in-progress*

Code Placement
==============

In order to maintain good code organization, testing scopes and dependency alignment.
We need to make sure that new code added to the software stack is integrated into the
software stack at the appropriate layer based on function, testing requirments, usage
and consumption, and impact/risk.  In order to help keep things in order, its important
to have some rules that help engineers make good decisions about where the code being
integrated belongs in the software stack.

Core
----

* Not specific to a manufacturer
* Should not require frequent changes

Integration
-----------
* Code enables inter-operation with enterprise resources
* Requires external shared resources to operate

Mid-Tier
--------
* Code is product specific
* Shared between teams
* Not test case code

Tests
-----
* Test case code
