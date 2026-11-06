"""Front panel brightness for Anthem receivers."""

from homeassistant.components.number import NumberEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AnthemavConfigEntry
from .entity import AnthemavReceiverEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AnthemavConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the panel brightness number (not supported on MDX)."""
    if config_entry.runtime_data.protocol.support_audio_listening_mode:
        async_add_entities([AnthemavPanelBrightness(config_entry)])


class AnthemavPanelBrightness(AnthemavReceiverEntity, NumberEntity):
    """Front panel brightness, 0 to 3."""

    _attr_translation_key = "panel_brightness"
    _attr_native_min_value = 0
    _attr_native_max_value = 3
    _attr_native_step = 1

    def __init__(self, config_entry: AnthemavConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(config_entry, "panel_brightness")

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        return self._avr.panel_brightness

    async def async_set_native_value(self, value: float) -> None:
        """Update the entity."""
        self._avr.panel_brightness = int(value)
