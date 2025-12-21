"""DataUpdateCoordinator for witty_one."""

from __future__ import annotations

from typing import Any

from homeassistant.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
)
from homeassistant.components.bluetooth.active_update_processor import (
    ActiveBluetoothProcessorCoordinator,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.witty_one.witty_one.parser import (
    WittyOneDevice,
    WittyOneDeviceData,
)

from .const import LOGGER

type WittyOneConfigEntry = ConfigEntry[
    ActiveBluetoothProcessorCoordinator[WittyOneDevice]
]

MAX_RETRY = 4
POLL_INTERVAL = 60


class WittyOneDataUpdateCoordinator(
    ActiveBluetoothProcessorCoordinator[WittyOneDevice]
):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: Any,
        logger: Any,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        address = config_entry.unique_id
        super().__init__(
            hass=hass,
            logger=logger,
            address=address,
            mode=BluetoothScanningMode.ACTIVE,
            update_method=self._handle_update,
            needs_poll_method=self._needs_poll,
            poll_method=self._async_poll_device,
        )
        self.witty = WittyOneDeviceData(logger)
        self.config_entry = config_entry
        self.nb_error = 0
        self.last_data: WittyOneDevice | None = None

    def _handle_update(
        self, _service_info: BluetoothServiceInfoBleak
    ) -> WittyOneDevice:
        """Update data from advertisements."""
        # Passive updates are not supported by Witty One, return existing data
        return self.last_data

    def _needs_poll(
        self,
        _service_info: BluetoothServiceInfoBleak,
        seconds_since_last_poll: float | None,
    ) -> bool:
        """Determine if a poll is needed."""
        return (
            seconds_since_last_poll is None or seconds_since_last_poll > POLL_INTERVAL
        )

    async def _async_poll_device(
        self, service_info: BluetoothServiceInfoBleak
    ) -> WittyOneDevice:
        """Poll the device."""
        try:
            data = await self.witty.update_device(service_info.device)
        except Exception as err:
            self.nb_error += 1
            if self.nb_error < MAX_RETRY and self.last_data:
                LOGGER.warning("Error updating device, using previous data: %s", err)
                return self.last_data
            msg = f"Unable to fetch data: {err}"
            raise UpdateFailed(msg) from err
        else:
            self.nb_error = 0
            self.last_data = data
            return data
