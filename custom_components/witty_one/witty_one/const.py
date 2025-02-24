"""Constants for witty one read."""

from uuid import UUID


def _info_uuid(address: str) -> UUID:
    return UUID(f"{address}e6d9-4a07-4169-a799-89bc59e4f742")


def _state_uuid(address: str) -> UUID:
    return UUID(f"{address}cf60-ea50-49f9-9471-a3fe0cfce893")


MODEL_UUID = _info_uuid("1400")

NAME_UUID = _state_uuid("0080")

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
