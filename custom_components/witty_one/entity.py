"""BlueprintEntity class."""

from __future__ import annotations

from homeassistant.components.bluetooth.passive_update_coordinator import (
    PassiveBluetoothCoordinatorEntity,
)
from homeassistant.helpers.device_registry import (
    CONNECTION_BLUETOOTH,
    DeviceInfo,
)

from .const import DOMAIN, MANUFACTURER
from .coordinator import WittyOneDataUpdateCoordinator
from .witty_one.parser import model_id_to_name


class WittyOneEntity(PassiveBluetoothCoordinatorEntity[WittyOneDataUpdateCoordinator]):
    """Define a base WittyOne Entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: WittyOneDataUpdateCoordinator, suffix: str) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._suffix = suffix
        self._attr_unique_id = f"{coordinator.config_entry.unique_id}_{suffix}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        data = self.coordinator.data
        if data is None:
            return DeviceInfo(
                connections={
                    (
                        CONNECTION_BLUETOOTH,
                        (str)(self.coordinator.config_entry.unique_id),
                    )
                },
                identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
                manufacturer=MANUFACTURER,
            )

        return DeviceInfo(
            connections={
                (CONNECTION_BLUETOOTH, (str)(self.coordinator.config_entry.unique_id))
            },
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            manufacturer=MANUFACTURER,
            name=data.static_information.name,
            model=model_id_to_name(data.static_information.model),
            model_id=data.static_information.model,
        )
