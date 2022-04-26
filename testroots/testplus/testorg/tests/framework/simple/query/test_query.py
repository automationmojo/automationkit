from akit.exceptions import akit_assert
from akit.testing import testplus

from akit.iterop.landscaping.landscapedevice import LandscapeDevice

def query_each_unique_device(apod):
    yielded_list = []

    all_devices = apod.landscape.get_devices()

    for dev in all_devices:
        if hasattr(dev, 'upnp') and dev.upnp is not None:
            model = dev.upnp.MODEL_NUMBER
            usn = dev.upnp.USN
            if model not in yielded_list:
                yielded_list.append(model)
                yield "{}:{}".format(model, usn)

@testplus.resource(query_function=query_each_unique_device)
def each_unique_device(apod) -> LandscapeDevice:
    yielded_list = []

    all_devices = apod.landscape.get_devices()

    for dev in all_devices:
        if hasattr(dev, 'upnp') and dev.upnp is not None:
            model = dev.upnp.MODEL_NUMBER
            if model not in yielded_list:
                yielded_list.append(model)

                apod.landscape.checkout_device(dev)

                yield dev

                apod.landscape.checkin_device(dev)

@testplus.param(each_unique_device, identifier='dev')
def test_checkout_and_checkin_by_model(apod, dev):

    errmsg = "The model number of the checked out device was device='{}'".format(dev)
    print(errmsg)

    return

