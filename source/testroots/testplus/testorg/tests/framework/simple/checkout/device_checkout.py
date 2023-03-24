
from akit.exceptions import akit_assert
from akit.testing import testplus

from akit.interop.landscaping.landscapedevice import LandscapeDevice

testplus.mark_descendent_priority(priority=0)

@testplus.resource()
def each_unique_model_number(apod) -> LandscapeDevice:
    yielded_list = []
    all_devices = apod.landscape.get_devices()
    for dev in all_devices:
        if hasattr(dev, 'upnp') and dev.upnp is not None:
            model = dev.upnp.MODEL_NUMBER
            if model not in yielded_list:
                yielded_list.append(model)
                yield model


@testplus.param(each_unique_model_number, identifier='model')
def test_checkout_and_checkin_by_model(apod, model):

    pre_avail = len( apod.landscape.list_available_devices())

    device = apod.landscape.checkout_a_device_by_modelNumber(model)

    post_avail = len( apod.landscape.list_available_devices())

    errmsg = "The post checkout count of available device pool devices should have decreased. exp={} found={}.".format(pre_avail, post_avail)
    akit_assert(pre_avail > post_avail, errmsg)

    apod.landscape.checkin_device(device)

    final_avail = len( apod.landscape.list_available_devices())

    errmsg = "The final count of available device pool devices should have restored to the original count. exp={} found={}.".format(pre_avail, final_avail)
    akit_assert(pre_avail == final_avail, errmsg)

    return

