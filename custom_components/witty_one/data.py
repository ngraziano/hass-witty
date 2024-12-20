"""Custom types for witty_one."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .coordinator import WittyOneDataUpdateCoordinator


type WittyOneConfigEntry = ConfigEntry[WittyOneData]


@dataclass
class WittyOneData:
    """Data for the Blueprint integration."""

    coordinator: WittyOneDataUpdateCoordinator
    integration: Integration
