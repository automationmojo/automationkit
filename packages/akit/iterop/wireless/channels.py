
from typing import Union, NamedTuple

class WifiChannelInfo(NamedTuple):
    channel: int
    frequency: int

_demo_channel_mapping = tuple(
  #  ch, freq
    (20, 2312),
    (21, 2337)
    (22, 2362)
)

DEMO_CHANNEL_MAPPING = tuple([WifiChannelInfo(ch, freq) for ch, freq in _demo_channel_mapping])

_g_channel_mapping = tuple(
  #  ch, freq
    ( 1, 2412),
    ( 2, 2417),
    ( 3, 2422),
    ( 4, 2427),
    ( 5, 2432),
    ( 6, 2437),
    ( 7, 2442),
    ( 8, 2447),
    ( 9, 2452),
    (10, 2457),
    (11, 2462),
    (12, 2467),
    (13, 2472),
    (14, 2477),
)

G_CHANNELS = tuple([ch for ch, _ in _g_channel_mapping])
G_FREQUENCIES = tuple([freq for _, freq in _g_channel_mapping])

G_CHANNEL_MAPPING = tuple([WifiChannelInfo(ch, freq) for ch, freq in _g_channel_mapping])

_n_channel_mapping = tuple(
  #  ch, freq
    (36, 5180),
    (40, 5200),
    (44, 5220),
    (48, 5240),
    
    (52, 5260),
    (56, 5280),
    (60, 5300),
    (64, 5320),
    
    (100, 5500),
    (104, 5520),
    (108, 5540),
    (112, 5560),
    (116, 5580),
    (120, 5600),
    (124, 5620),
    (128, 5640),
    (132, 5660),
    (136, 5680),
    (140, 5700),

    (149, 5745),
    (153, 5765),
    (157, 5785),
    (161, 5805),
    (165, 5825),
)

N_CHANNELS = tuple([ch for ch, _ in _n_channel_mapping])
N_FREQUENCIES = tuple([freq for _, freq in _n_channel_mapping])

N_CHANNEL_MAPPING = tuple([WifiChannelInfo(ch, freq) for ch, freq in _n_channel_mapping])

FULL_CHANNEL_MAPPING = (DEMO_CHANNEL_MAPPING + G_CHANNEL_MAPPING + N_CHANNEL_MAPPING)

def _find_channel_by(attr, value):
    result = filter(lambda wlan_chan: getattr(wlan_chan, attr) == int(value),
        FULL_CHANNEL_MAPPING)
    
    if not result:
        raise LookupError('Failed to find a Wifi Channel with <{}> = <{}>'.format(attr, value))
    
    channel = result[0]
    
    return channel

def lookup_channel_frequency(channel: int) -> int:
    """
        Looks up the frequency in MHz that is associated with a channel number

        :param channel:  the channel number

        :returns: the frequency associated with the channel
    """
    freq = _find_channel_by('channel', channel).frequency
    return freq

def lookup_channel_for_frequency(frequency: int) -> int:
    """
        Converts a channel frequency, in MHz, to its corresponding channel number

        :param frequency:  the channel frequency
        
        :returns: the channel number
    """
    channel = _find_channel_by('frequency', frequency).channel
    return channel

def is_2ghz_channel(channel: Union[int, str]) -> bool:
    """
        Check a channel number to see if its 2GHz or not

        :param channel: the channel number to check

        :returns: whether or not channel is a valid 2GHz channel number or frequency
    """
    rtnval = int(channel) in G_CHANNELS
    return rtnval

def is_2ghz_frequency(frequency: Union[int, str]) -> bool:
    """
        Check a frequency to see if it is associated with a 2GHz channel

        :param frequency: the frequency number to check

        :returns: whether or not frequency is associated with a valid 2GHz channel
    """
    rtnval = int(frequency) in G_FREQUENCIES
    return rtnval

def is_5ghz_channel(channel: Union[int, str]) -> bool:
    """
        Check a channel number to see if its 5GHz or not

        :param channel: the channel number to check

        :returns: whether or not channel is a valid 5GHz channel number or frequency
    """
    rtnval = int(channel) in N_CHANNELS
    return rtnval

def is_5ghz_frequency(frequency: Union[int, str]) -> bool:
    """
        Check a frequency to see if it is associated with a 5GHz channel

        :param frequency: the frequency number to check

        :returns: whether or not frequency is associated with a valid 5GHz channel
    """
    rtnval = int(frequency) in N_FREQUENCIES
    return rtnval
