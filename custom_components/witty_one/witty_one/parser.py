"""Parser for Witty One device."""

import asyncio
import dataclasses
import struct
from logging import Logger
from typing import Any
from uuid import UUID

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection

from .const import (
    AMBIENT_TEMP_UUID,
    ELECTRIC_STATE_UUID,
    ENERGY_UUID,
    MODEL_UUID,
    NAME_UUID,
    RELAY_TEMP_UUID,
    SESSION_STATE_UUID,
    STATE_UUID,
)


@dataclasses.dataclass
class WittyOneStaticProperties:
    """Static informations."""

    name: str = ""
    model: str = ""


@dataclasses.dataclass
class WittyOnePhaseEnergy:
    """Different energies for one phase."""

    active_import_energy: float = 0.0
    active_export_energy: float = 0.0
    reactive_import_energy: float = 0.0
    reactive_export_energy: float = 0.0
    apparent_energy: float = 0.0


@dataclasses.dataclass
class WittyOnePhaseState:
    """Voltage, current, power and power factor for one phase."""

    voltage: float = 0.0
    current: float = 0.0
    active_power: float = 0.0
    apparent_power: float = 0.0
    reactive_power: float = 0.0
    power_factor: float = 0.0
    cos_phi: float = 0.0
    quadrant: int = 0
    frequency: float = 0.0


@dataclasses.dataclass
class WittyCurrentSession:
    """Current session data for Witty One device."""

    start: int = 0
    unk1: bytes = b""
    duration: int = 0
    energy: float = 0.0
    unk3: int = 0
    badge: bytes = b""


@dataclasses.dataclass
class WittyOneGeneralState:
    """General state data for Witty One device."""

    mainstate: int = 0
    substate: int = 0


@dataclasses.dataclass
class WittyOneDevice:
    """Reponse data for Witty One device."""

    static_information: WittyOneStaticProperties
    general: WittyOneGeneralState = dataclasses.field(
        default_factory=WittyOneGeneralState
    )
    energies: list[WittyOnePhaseEnergy] = dataclasses.field(default_factory=list)
    phases_states: list[WittyOnePhaseState] = dataclasses.field(default_factory=list)
    current_session: WittyCurrentSession = dataclasses.field(
        default_factory=WittyCurrentSession
    )


class ParseError(Exception):
    """Error during parse."""


async def _read_string(client: BleakClient, uuid: str | UUID) -> str:
    tmp = await client.read_gatt_char(uuid)
    (length,) = struct.unpack("<H", tmp[0:2])
    return tmp[2 : 2 + length].rstrip(b"\0").decode("utf-8")


def _unpack(fmt: str, buffer: bytearray) -> tuple[Any, ...]:
    try:
        return struct.unpack(fmt, buffer)
    except struct.error as err:
        msg = f"witty_one wanted {fmt} receive buffer[{len(buffer)}] {buffer.hex()}"
        raise ParseError(msg) from err


async def _read_static_properties(client: BleakClient) -> WittyOneStaticProperties:
    (
        name,
        model,
    ) = await asyncio.gather(
        _read_string(client, NAME_UUID),
        _read_string(client, MODEL_UUID),
    )
    return WittyOneStaticProperties(
        name=name,
        model=model,
    )


async def _read_energy(client: BleakClient) -> list[WittyOnePhaseEnergy]:
    tmp = await client.read_gatt_char(ENERGY_UUID)
    values = _unpack("<HQQQQQQQQQQQQQQQQQQQQ", tmp)
    return [
        WittyOnePhaseEnergy(
            active_import_energy=values[1] / 1000,
            active_export_energy=values[2] / 1000,
            reactive_import_energy=values[3] / 1000,
            reactive_export_energy=values[4] / 1000,
            apparent_energy=values[5] / 1000,
        ),
        WittyOnePhaseEnergy(
            active_import_energy=values[6] / 1000,
            active_export_energy=values[7] / 1000,
            reactive_import_energy=values[8] / 1000,
            reactive_export_energy=values[9] / 1000,
            apparent_energy=values[10] / 1000,
        ),
        WittyOnePhaseEnergy(
            active_import_energy=values[11] / 1000,
            active_export_energy=values[12] / 1000,
            reactive_import_energy=values[13] / 1000,
            reactive_export_energy=values[14] / 1000,
            apparent_energy=values[15] / 1000,
        ),
        WittyOnePhaseEnergy(
            active_import_energy=values[16] / 1000,
            active_export_energy=values[17] / 1000,
            reactive_import_energy=values[18] / 1000,
            reactive_export_energy=values[19] / 1000,
            apparent_energy=values[20] / 1000,
        ),
    ]


async def _read_phases_state(client: BleakClient) -> list[WittyOnePhaseState]:
    tmp = await client.read_gatt_char(ELECTRIC_STATE_UUID)
    values = _unpack("<Hlllllllllllllllllllllllllllllll", tmp)
    return [
        WittyOnePhaseState(
            voltage=values[1] / 1000,
            current=values[2] / 1000,
            active_power=values[3] / 1000,
            apparent_power=values[4] / 1000,
            reactive_power=values[5] / 1000,
            power_factor=values[6] / 1000,
            cos_phi=values[7] / 1000,
            quadrant=values[8],
        ),
        WittyOnePhaseState(
            voltage=values[9] / 1000,
            current=values[10] / 1000,
            active_power=values[11] / 1000,
            apparent_power=values[12] / 1000,
            reactive_power=values[13] / 1000,
            power_factor=values[14] / 1000,
            cos_phi=values[15] / 1000,
            quadrant=values[16],
        ),
        WittyOnePhaseState(
            voltage=values[17] / 1000,
            current=values[18] / 1000,
            active_power=values[19] / 1000,
            apparent_power=values[20] / 1000,
            reactive_power=values[21] / 1000,
            power_factor=values[22] / 1000,
            cos_phi=values[23] / 1000,
            quadrant=values[24],
        ),
        WittyOnePhaseState(
            active_power=values[25] / 1000,
            apparent_power=values[26] / 1000,
            reactive_power=values[27] / 1000,
            power_factor=values[28] / 1000,
            cos_phi=values[29] / 1000,
            quadrant=values[30],
            frequency=values[31] / 1000,
        ),
    ]


async def _current_session(client: BleakClient) -> WittyCurrentSession:
    tmp = await client.read_gatt_char(SESSION_STATE_UUID)
    values = struct.unpack_from("<HL7sLQB7s", tmp)
    return WittyCurrentSession(
        start=values[1],
        unk1=values[2],
        duration=values[3],
        energy=values[4] / 1000,
        unk3=values[5],
        badge=values[6],
    )


async def _read_general_state(client: BleakClient) -> WittyOneGeneralState:
    tmp = await client.read_gatt_char(STATE_UUID)
    values = struct.unpack_from("<HI", tmp)
    return WittyOneGeneralState(mainstate=values[1] >> 8, substate=values[1] & 0xFF)


async def _ambient_temp(client: BleakClient) -> float:
    tmp = await client.read_gatt_char(AMBIENT_TEMP_UUID)
    (_, value, _min_value, _max_value) = _unpack("<Hhhh", tmp)
    return value / 100


async def _relay_temp(client: BleakClient) -> float:
    tmp = await client.read_gatt_char(RELAY_TEMP_UUID)
    (_, value, _min_value, _max_value) = _unpack("<Hhhh", tmp)
    return value / 100


class WittyOneDeviceData:
    """Data for Witty One device."""

    static_properties: WittyOneStaticProperties | None = None

    def __init__(
        self,
        logger: Logger,
    ) -> None:
        """Initialize the WittyOneDeviceData with a logger."""
        super().__init__()
        self.logger = logger

    async def update_device(self, ble_device: BLEDevice) -> WittyOneDevice:
        """Update the device."""
        client = await establish_connection(BleakClient, ble_device, ble_device.address)
        await client.pair()

        if self.static_properties is None:
            try:
                self.static_properties = await _read_static_properties(client)
            except Exception:
                self.logger.exception("Fail to read static info")
                self.logger.warning(
                    'try to add CONFIG_BT_GATTC_MAX_CACHE_CHAR: "80"'
                    " to sdkconfig_options if you use esphome"
                )
                if callable(getattr(client, "clear_cache", None)):
                    await client.clear_cache()  # pyright: ignore[reportAttributeAccessIssue]
                raise

        device = WittyOneDevice(static_information=self.static_properties)

        try:
            (
                device.general,
                device.energies,
                device.phases_states,
                device.current_session,
            ) = await asyncio.gather(
                _read_general_state(client),
                _read_energy(client),
                _read_phases_state(client),
                _current_session(client),
            )
        except ParseError:
            self.logger.exception("Fail to read dynamic info, cache cleared, try again")
            if callable(getattr(client, "clear_cache", None)):
                await client.clear_cache()  # pyright: ignore[reportAttributeAccessIssue]
            raise

        self.logger.debug("Device data: %s", device)
        await client.disconnect()
        return device


def model_id_to_name(model_id: str) -> str:
    """Convert model id to a string."""
    match model_id:
        case "XVR111STI":
            return "Witty one 1x11kW 3P"
        case "XVR107STP":
            return "Witty one 1x7kW 1P"
        case "XVR107STI":
            return "Witty one 1x7kW 1P"
        case _:
            return "Witty unknown"
