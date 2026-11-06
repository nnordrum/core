"""Input format sensors for Anthem receivers."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AnthemavConfigEntry
from .entity import AnthemavReceiverEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AnthemavConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up input format sensors (not supported on MDX)."""
    if not config_entry.runtime_data.protocol.support_audio_listening_mode:
        return
    async_add_entities(
        [
            AnthemavFormatSensor(
                config_entry, "audio_format", "audio_input_format_text"
            ),
            AnthemavFormatSensor(
                config_entry, "audio_channels", "audio_input_channels_text"
            ),
            AnthemavFormatSensor(
                config_entry, "video_resolution", "video_input_resolution_text"
            ),
        ]
    )


class AnthemavFormatSensor(AnthemavReceiverEntity, SensorEntity):
    """Text reported by the receiver for the current input format."""

    def __init__(self, config_entry: AnthemavConfigEntry, key: str, prop: str) -> None:
        """Initialize the entity."""
        super().__init__(config_entry, key)
        self._attr_translation_key = key
        self._prop = prop

    @property
    def native_value(self) -> str | None:
        """Return the current value."""
        return getattr(self._avr, self._prop) or None
