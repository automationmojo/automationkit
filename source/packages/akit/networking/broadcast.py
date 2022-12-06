
def broadcast_wake_on_lan_magic_message(brodcast_addr: str, mac_addr: str):
    '[FF FF FF FF FF FF] + [mac] * 16   ( len 102 bytes )'
    return