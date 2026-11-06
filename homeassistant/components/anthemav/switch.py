"""Standby IP control and ARC room correction switches."""

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AnthemavConfigEntry
from .entity import AnthemavReceiverEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AnthemavConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up receiver switches (not supported on MDX)."""
    if not config_entry.runtime_data.protocol.support_audio_listening_mode:
        return
    async_add_entities(
        [
            AnthemavStandbyIPControl(config_entry),
            AnthemavARC(config_entry),
        ]
    )


class AnthemavStandbyIPControl(AnthemavReceiverEntity, SwitchEntity):
    """Keep the receiver reachable over IP in standby."""

    _attr_translation_key = "standby_ip_control"

    def __init__(self, config_entry: AnthemavConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(config_entry, "standby_ip_control")

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return bool(self._avr.standby_control)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Update the entity."""
        self._avr.standby_control = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Update the entity."""
        self._avr.standby_control = False


class AnthemavARC(AnthemavReceiverEntity, SwitchEntity):
    """Anthem Room Correction."""

    _attr_translation_key = "arc"

    def __init__(self, config_entry: AnthemavConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(config_entry, "arc")

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return bool(self._avr.arc)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Update the entity."""
        self._avr.arc = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Update the entity."""
        self._avr.arc = False
