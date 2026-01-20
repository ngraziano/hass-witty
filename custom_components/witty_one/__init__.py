"""
Custom integration to integrate witty_one with Home Assistant.

For more details about this integration, please refer to
https://github.com/ngraziano/hass-witty
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform

from .const import LOGGER
from .coordinator import WittyOneProcessorCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .coordinator import WittyOneConfigEntry

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: WittyOneConfigEntry) -> bool:
    """Set up this integration using UI."""
    coordinator = entry.runtime_data = WittyOneProcessorCoordinator(
        hass=hass,
        logger=LOGGER,
        config_entry=entry,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(coordinator.async_start())
    return True


async def async_unload_entry(hass: HomeAssistant, entry: WittyOneConfigEntry) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
