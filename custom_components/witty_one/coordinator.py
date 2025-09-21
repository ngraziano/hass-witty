"""DataUpdateCoordinator for witty_one."""

from __future__ import annotations

from typing import Any

from bleak_retry_connector import (
    close_stale_connections_by_address,
)
from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryError, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.witty_one.witty_one.parser import (
    WittyOneDevice,
    WittyOneDeviceData,
)

from .const import LOGGER

type WittyOneConfigEntry = ConfigEntry[WittyOneDataUpdateCoordinator]

MAX_RETRY = 4


class WittyOneDataUpdateCoordinator(DataUpdateCoordinator[WittyOneDevice]):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry
    witty = WittyOneDeviceData(LOGGER)

    previsous_data: WittyOneDevice | None = None
    nb_error = 0

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        address = self.config_entry.unique_id
        if not address:
            msg = "No address found in configuration"
            raise ConfigEntryNotReady(msg)

        LOGGER.debug("Updating data from %s ", address)

        await close_stale_connections_by_address(address)

        ble_device = bluetooth.async_ble_device_from_address(self.hass, address)
        if not ble_device:
            self.nb_error += 1
            if self.nb_error < MAX_RETRY and self.previsous_data:
                LOGGER.warning("Device not found, using previous data")
                return self.previsous_data
            msg = f"Could not find Witty One device with address {address}"
            raise ConfigEntryError(msg)

        try:
            data = await self.witty.update_device(ble_device)
        except Exception as err:
            self.nb_error += 1
            if self.nb_error < MAX_RETRY and self.previsous_data:
                LOGGER.warning("Error updating device, using previous data: %s", err)
                return self.previsous_data
            msg = f"Unable to fetch data: {err}"
            raise UpdateFailed(msg) from err

        self.previsous_data = data
        self.nb_error = 0
        return data
