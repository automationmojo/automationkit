
from akit.testing import testplus

from integrations.upnpcoord import upnp_coordinator_integration

from testorg.scopes.automationpod import automation_pod

testplus.originate_parameter(upnp_coordinator_integration, identifier="upnp_integ")
testplus.originate_parameter(automation_pod, identifier="apod")
