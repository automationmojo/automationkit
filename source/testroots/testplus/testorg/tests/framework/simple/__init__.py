
from akit.testing import testplus

from testorg.integrations.upnpcoord import upnp_coordinator_integration
from testorg.services.webserver import http_content_server
from testorg.scopes.automationpod import automation_pod

testplus.originate_parameter(upnp_coordinator_integration, identifier="upnp_integ")
testplus.originate_parameter(http_content_server, identifier='http_csrv')
testplus.originate_parameter(automation_pod, identifier="apod")
