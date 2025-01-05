"""Sensor platform for witty_one."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfTime

from .entity import WittyOneEntity

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

    from custom_components.witty_one.witty_one.parser import WittyOneDevice

    from .coordinator import WittyOneDataUpdateCoordinator
    from .data import WittyOneConfigEntry


@dataclass(frozen=True, kw_only=True)
class WittyOneSensorEntityDescription(SensorEntityDescription):
    """Describes WLED sensor entity."""

    exists_fn: Callable[[WittyOneDevice], bool] = lambda _: True
    value_fn: Callable[[WittyOneDevice], datetime | StateType]


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
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: WittyOneConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        WittyOneSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
        if entity_description.exists_fn(coordinator.data)
    )


class WittyOneSensor(WittyOneEntity, SensorEntity):
    """witty_one Sensor class."""

    entity_description: WittyOneSensorEntityDescription

    def __init__(
        self,
        coordinator: WittyOneDataUpdateCoordinator,
        entity_description: WittyOneSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, entity_description.key)
        self.entity_description = entity_description

    @property
    def native_value(self) -> datetime | StateType:
        """Return the native value of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
