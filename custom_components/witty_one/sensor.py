"""Sensor platform for witty_one."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataProcessor,
    PassiveBluetoothDataUpdate,
    PassiveBluetoothEntityKey,
    PassiveBluetoothProcessorEntity,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.helpers.device_registry import CONNECTION_BLUETOOTH, DeviceInfo

from .const import DOMAIN, MANUFACTURER
from .witty_one.parser import model_id_to_name

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

    from custom_components.witty_one.witty_one.parser import WittyOneDevice

    from .coordinator import WittyOneConfigEntry


@dataclass(frozen=True, kw_only=True)
class WittyOneSensorEntityDescription(SensorEntityDescription):
    """Describes Witty One sensor entity."""

    exists_fn: Callable[[WittyOneDevice], bool] = lambda _: True
    value_fn: Callable[[WittyOneDevice], datetime | StateType]


GENERAL_STATES = {
    1: "idle",
    2: "wait",
    4: "wait_energy",
    6: "charging",
    8: "finish",
    16: "reserved",
    15728640: "error",
}

ENTITY_DESCRIPTIONS: tuple[WittyOneSensorEntityDescription, ...] = (
    WittyOneSensorEntityDescription(
        key="total_energy",
        translation_key="total_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda device: device.energies[3].active_import_energy,
    ),
    WittyOneSensorEntityDescription(
        key="phase1_energy",
        translation_key="phase1_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda device: device.energies[0].active_import_energy,
    ),
    WittyOneSensorEntityDescription(
        key="phase2_energy",
        translation_key="phase2_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda device: device.energies[1].active_import_energy,
    ),
    WittyOneSensorEntityDescription(
        key="phase3_energy",
        translation_key="phase3_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda device: device.energies[2].active_import_energy,
    ),
    WittyOneSensorEntityDescription(
        key="current_session_energy",
        translation_key="current_session_energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        value_fn=lambda device: device.current_session.energy,
    ),
    WittyOneSensorEntityDescription(
        key="power",
        translation_key="power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.phases_states[3].active_power,
    ),
    WittyOneSensorEntityDescription(
        key="current_session_duration",
        translation_key="current_session_duration",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        value_fn=lambda device: device.current_session.duration,
    ),
    WittyOneSensorEntityDescription(
        key="state",
        translation_key="state",
        device_class=SensorDeviceClass.ENUM,
        options=list(GENERAL_STATES.values()),
        value_fn=lambda device: GENERAL_STATES[device.general.mainstate],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: WittyOneConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data

    def _sensor_update_to_bluetooth_data_update(
        data: WittyOneDevice | None,
    ) -> PassiveBluetoothDataUpdate:
        """Convert a sensor update to a bluetooth data update."""
        device_info = DeviceInfo(
            connections={(CONNECTION_BLUETOOTH, coordinator.address)},
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer=MANUFACTURER,
        )
        if data:
            device_info.update(
                {
                    "name": data.static_information.name,
                    "model": model_id_to_name(data.static_information.model),
                    "model_id": data.static_information.model,
                }
            )

        return PassiveBluetoothDataUpdate(
            devices={coordinator.address: device_info},
            entity_descriptions={
                PassiveBluetoothEntityKey(
                    desc.key, coordinator.address
                ): SensorEntityDescription(
                    key=desc.key,
                    device_class=desc.device_class,
                    native_unit_of_measurement=desc.native_unit_of_measurement,
                    state_class=desc.state_class,
                    translation_key=desc.translation_key,
                    options=desc.options,
                )
                for desc in ENTITY_DESCRIPTIONS
                if data is None or desc.exists_fn(data)
            },
            entity_data={
                PassiveBluetoothEntityKey(desc.key, coordinator.address): desc.value_fn(
                    data
                )
                for desc in ENTITY_DESCRIPTIONS
                if data and desc.exists_fn(data)
            },
            entity_names={},
        )

    processor = PassiveBluetoothDataProcessor(_sensor_update_to_bluetooth_data_update)
    entry.async_on_unload(
        processor.async_add_entities_listener(WittyOneSensor, async_add_entities)
    )
    entry.async_on_unload(
        coordinator.async_register_processor(processor, SensorEntityDescription)
    )


class WittyOneSensor(PassiveBluetoothProcessorEntity[Any], SensorEntity):
    """witty_one Sensor class."""

    _attr_has_entity_name = True

    @property
    def native_value(self) -> datetime | StateType:
        """Return the native value of the sensor."""
        return self.processor.entity_data.get(self.entity_key)
