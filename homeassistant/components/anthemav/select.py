"""Select entities for Anthem receiver settings."""

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AnthemavConfigEntry
from .entity import AnthemavReceiverEntity

DYNAMIC_RANGE_OPTIONS = ["Normal", "Reduced", "Late Night"]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AnthemavConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up receiver select entities (not supported on MDX)."""
    avr = config_entry.runtime_data.protocol
    if not avr.support_audio_listening_mode:
        return
    async_add_entities(
        [
            AnthemavListeningMode(config_entry),
            AnthemavDolbyDynamicRange(config_entry),
        ]
    )


class AnthemavListeningMode(AnthemavReceiverEntity, SelectEntity):
    """Audio listening mode."""

    _attr_translation_key = "listening_mode"

    def __init__(self, config_entry: AnthemavConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(config_entry, "listening_mode")

    @property
    def options(self) -> list[str]:
        """Return the selectable options."""
        return self._avr.audio_listening_mode_list

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        return self._avr.audio_listening_mode_text

    async def async_select_option(self, option: str) -> None:
        """Update the entity."""
        self._avr.audio_listening_mode_text = option


class AnthemavDolbyDynamicRange(AnthemavReceiverEntity, SelectEntity):
    """Dolby digital dynamic range."""

    _attr_translation_key = "dolby_dynamic_range"

    def __init__(self, config_entry: AnthemavConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(config_entry, "dolby_dynamic_range")

    @property
    def options(self) -> list[str]:
        """Return the selectable options."""
        return DYNAMIC_RANGE_OPTIONS

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        text = self._avr.dolby_dynamic_range_text
        return text if text in DYNAMIC_RANGE_OPTIONS else None

    async def async_select_option(self, option: str) -> None:
        """Update the entity."""
        self._avr.dolby_dynamic_range = DYNAMIC_RANGE_OPTIONS.index(option)
