"""Test receiver-level entities (listening mode, Dolby, panel brightness, switches, sensors)."""

from unittest.mock import AsyncMock

import pytest
from pytest_homeassistant.common import MockConfigEntry

from homeassistant.components.media_player import MediaPlayerEntityFeature
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_OPTION,
    STATE_OFF,
    STATE_ON,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

RECEIVER_PLATFORMS = [
    Platform.MEDIA_PLAYER,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]


@pytest.mark.parametrize("platforms", [RECEIVER_PLATFORMS])
async def test_receiver_entities_created(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    init_integration: MockConfigEntry,
) -> None:
    """Receiver-level entities are created on the receiver device."""
    mac = "00:00:00:00:00:01"
    assert entity_registry.async_get_entity_id(
        "select", "anthemav", f"{mac}_listening_mode"
    )
    assert entity_registry.async_get_entity_id(
        "select", "anthemav", f"{mac}_dolby_dynamic_range"
    )
    assert entity_registry.async_get_entity_id(
        "number", "anthemav", f"{mac}_panel_brightness"
    )
    assert entity_registry.async_get_entity_id(
        "switch", "anthemav", f"{mac}_standby_ip_control"
    )
    assert entity_registry.async_get_entity_id("switch", "anthemav", f"{mac}_arc")
    assert entity_registry.async_get_entity_id(
        "sensor", "anthemav", f"{mac}_audio_format"
    )


@pytest.mark.parametrize("platforms", [RECEIVER_PLATFORMS])
async def test_volume_step_feature(
    hass: HomeAssistant, init_integration: MockConfigEntry
) -> None:
    """Every zone advertises volume step so volume_up/volume_down work."""
    state = hass.states.get("media_player.anthem_av")
    assert state
    assert state.attributes["supported_features"] & MediaPlayerEntityFeature.VOLUME_STEP


@pytest.mark.parametrize("platforms", [RECEIVER_PLATFORMS])
async def test_set_panel_brightness(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
    mock_anthemav: AsyncMock,
) -> None:
    """Setting panel brightness reaches the receiver."""
    await hass.services.async_call(
        "number",
        "set_value",
        {ATTR_ENTITY_ID: "number.anthem_av_panel_brightness", "value": 2},
        blocking=True,
    )
    assert mock_anthemav.protocol.panel_brightness == 2


@pytest.mark.parametrize("platforms", [RECEIVER_PLATFORMS])
async def test_set_listening_mode(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
    mock_anthemav: AsyncMock,
) -> None:
    """Selecting a listening mode sets it on the receiver."""
    mock_anthemav.protocol.audio_listening_mode_list = ["Dolby Surround", "Stereo"]
    await hass.services.async_call(
        "select",
        "select_option",
        {
            ATTR_ENTITY_ID: "select.anthem_av_listening_mode",
            ATTR_OPTION: "Dolby Surround",
        },
        blocking=True,
    )
    assert mock_anthemav.protocol.audio_listening_mode_text == "Dolby Surround"


@pytest.mark.parametrize("platforms", [RECEIVER_PLATFORMS])
async def test_arc_switch(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
    mock_anthemav: AsyncMock,
) -> None:
    """ARC switch toggles the receiver setting."""
    await hass.services.async_call(
        "switch",
        "turn_on",
        {ATTR_ENTITY_ID: "switch.anthem_av_arc_room_correction"},
        blocking=True,
    )
    assert mock_anthemav.protocol.arc is True
    state = hass.states.get("switch.anthem_av_arc_room_correction")
    assert state
    assert state.state in (STATE_ON, STATE_OFF)
