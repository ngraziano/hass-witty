"""BlueprintEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import MANUFACTURER
from .coordinator import WittyOneDataUpdateCoordinator


class WittyOneEntity(CoordinatorEntity[WittyOneDataUpdateCoordinator]):
    """WittyOneEntity class."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: WittyOneDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            connections={
                (
                    CONNECTION_NETWORK_MAC,
                    (str)(coordinator.config_entry.unique_id),
                ),
            },
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
            manufacturer=MANUFACTURER,
        )
