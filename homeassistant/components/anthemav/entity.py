"""Base class for receiver-level entities (attached to the receiver device, not a zone)."""

from typing import override

from homeassistant.const import CONF_MAC
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from . import AnthemavConfigEntry
from .const import ANTHEMAV_UPDATE_SIGNAL, DOMAIN


class AnthemavReceiverEntity(Entity):
    """Receiver-level entity; refreshed on every receiver update."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, config_entry: AnthemavConfigEntry, key: str) -> None:
        """Initialize the entity on the receiver device."""
        mac_address = config_entry.data[CONF_MAC]
        self._avr = config_entry.runtime_data.protocol
        self._entry_id = config_entry.entry_id
        self._attr_unique_id = f"{mac_address}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, mac_address)},
            connections={(dr.CONNECTION_NETWORK_MAC, mac_address)},
        )

    @override
    async def async_added_to_hass(self) -> None:
        """Subscribe to receiver updates."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"{ANTHEMAV_UPDATE_SIGNAL}_{self._entry_id}",
                self._handle_update,
            )
        )

    @callback
    def _handle_update(self) -> None:
        """Write the new state."""
        self.async_write_ha_state()
