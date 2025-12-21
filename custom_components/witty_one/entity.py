"""BlueprintEntity class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothEntityKey,
    PassiveBluetoothProcessorEntity,
)

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class WittyOneEntity(PassiveBluetoothProcessorEntity[Any]):
    """Define a base WittyOne Entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        processor: Any,
        entity_key: PassiveBluetoothEntityKey,
        description: EntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(processor, entity_key, description)
        self._attr_unique_id = f"{entity_key.device_id}_{description.key}"
