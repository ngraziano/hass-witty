"""Parser for Witty One device."""

import dataclasses
import struct
from logging import Logger

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection


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
class WittyOneDevice:
    """Reponse data for Witty One device."""

    energies: list[WittyOnePhaseEnergy] = dataclasses.field(default_factory=list)
    phases_states: list[WittyOnePhaseState] = dataclasses.field(default_factory=list)
    current_session: WittyCurrentSession = dataclasses.field(
        default_factory=WittyCurrentSession
    )


class WittyOneDeviceData:
    """Data for Witty One device."""

    def __init__(
        self,
        logger: Logger,
    ) -> None:
        """Initialize the WittyOneDeviceData with a logger."""
        super().__init__()
        self.logger = logger

    async def _update_energy(self, client: BleakClient) -> list[WittyOnePhaseEnergy]:
        tmp = await client.read_gatt_char("4010cf60-ea50-49f9-9471-a3fe0cfce893")
        values = struct.unpack("<HQQQQQQQQQQQQQQQQQQQQ", tmp)
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

    async def _update_phases_state(
        self, client: BleakClient
    ) -> list[WittyOnePhaseState]:
        tmp = await client.read_gatt_char("4110cf60-ea50-49f9-9471-a3fe0cfce893")
        values = struct.unpack("<HLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL", tmp)
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

    async def _current_session(self, client: BleakClient) -> WittyCurrentSession:
        tmp = await client.read_gatt_char("6110cf60-ea50-49f9-9471-a3fe0cfce893")
        values = struct.unpack_from("<HL7sLQB7s", tmp)
        return WittyCurrentSession(
            start=values[1],
            unk1=values[2],
            duration=values[3],
            energy=values[4] / 1000,
            unk3=values[5],
            badge=values[6],
        )

    async def update_device(self, ble_device: BLEDevice) -> WittyOneDevice:
        """Update the device."""
        client = await establish_connection(BleakClient, ble_device, ble_device.address)
        device = WittyOneDevice()
        await client.pair()

        device.energies = await self._update_energy(client)
        device.phases_states = await self._update_phases_state(client)
        device.current_session = await self._current_session(client)
        self.logger.debug("Device data: %s", device)
        await client.disconnect()
        return device