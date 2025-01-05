"""BlueprintEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import (
    CONNECTION_BLUETOOTH,
    DeviceInfo,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import WittyOneDataUpdateCoordinator


class WittyOneEntity(CoordinatorEntity[WittyOneDataUpdateCoordinator]):
    """Define a base WittyOne Entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: WittyOneDataUpdateCoordinator, suffix: str) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self._attr_unique_id = f"{coordinator.config_entry.unique_id}_{suffix}"
        self._attr_device_info = DeviceInfo(
            connections={
                (CONNECTION_BLUETOOTH, (str)(coordinator.config_entry.unique_id))
            },
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer=MANUFACTURER,
            name=coordinator.config_entry.title,
        )
