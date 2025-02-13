"""Constants for witty one read."""


def _state_uuid(address: str) -> str:
    return f"{address}cf60-ea50-49f9-9471-a3fe0cfce893"


# Version
# app version a.b.c.d _
# length 4+0x0005 format <HBBBBB
PACKAGE_VERSION_UUID = _state_uuid("0002")

# app version a.b.c.d (_) boot version a.b.c.d
# length 4+0x003C format <HBBBBBBBB...
MAIN_BOARD_VERSION_UUID = _state_uuid("0102")
RF_BOARD_VERSION_UUID = _state_uuid("0202")
HMI_BOARD_VERSION_UUID = _state_uuid("0302")

STARTUP_COUNT_UUID = _state_uuid("0410")  # length 4+0x0004 format : <HQ
DURATIONS_UUID = _state_uuid("0510")  # length 4+0x0010 format : <HIIII
COMMUTATION_UUID = _state_uuid("0610")  # length 4+0x0020 format : <HQQQQ


# Electric
ENERGY_UUID = _state_uuid("4010")
ELECTRIC_STATE_UUID = _state_uuid("4110")

# Temp
AMBIENT_TEMP_UUID = _state_uuid("5010")
RELAY_TEMP_UUID = _state_uuid("5110")


SESSION_STATE_UUID = _state_uuid("6110")
