"""DataUpdateCoordinator for witty_one."""

from __future__ import annotations

from datetime import timedelta
import struct
from typing import TYPE_CHECKING, Any

from bleak import BleakClient
from bleak_retry_connector import establish_connection
from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class WittyOneDataUpdateCoordinator(DataUpdateCoordinator[ConfigEntry]):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

    async def _async_setup(self) -> None:
        """Set up the data."""
        pass
        # self.config_entry.unique_id

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        LOGGER.info("Updating data from %s ", self.config_entry)
        LOGGER.info(self.config_entry)
        address = self.config_entry.unique_id

        assert address is not None

        ble_device = bluetooth.async_ble_device_from_address(self.hass, address)
        assert ble_device is not None

        client = await establish_connection(BleakClient, ble_device, ble_device.address)
        await client.pair()
        tmp = await client.read_gatt_char("4010cf60-ea50-49f9-9471-a3fe0cfce893")
        d = struct.unpack("<HQQQQQQQQQQQQQQQQQQQQ", tmp)[20]
        LOGGER.info("Data: %s", tmp)
        await client.disconnect()
        return {"body": d / 1000}
        # try:
        #    return await self.config_entry.runtime_data.client.async_get_data()
        # except WittyOneApiClientAuthenticationError as exception:
        #    raise ConfigEntryAuthFailed(exception) from exception
        # except WittyOneApiClientError as exception:
        #     raise UpdateFailed(exception) from exception
