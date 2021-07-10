
from akit.testing import testplus

from testorg.rooms.hometheater import hometheater_room
from testorg.services.webserver import http_content_server

testplus.register_wellknown_parameter(hometheater_room, identifier="ht_room", constraints={"players": ["S9", "S10"]})
testplus.register_wellknown_parameter(http_content_server, identifier="websrv")
