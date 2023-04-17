"""Provide common tests tools for tts."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.tts import (
    CONF_LANG,
    PLATFORM_SCHEMA,
    Provider,
    TextToSpeechEntity,
    TtsAudioType,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from tests.common import MockPlatform

SUPPORT_LANGUAGES = ["de", "en", "en_US"]

DEFAULT_LANG = "en"


class BaseProvider:
    """Test speech API provider."""

    def __init__(self, lang: str) -> None:
        """Initialize test provider."""
        self._lang = lang

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options like voice, emotions."""
        return ["voice", "age"]

    def get_tts_audio(
        self, message: str, language: str, options: dict[str, Any] | None = None
    ) -> TtsAudioType:
        """Load TTS dat."""
        return ("mp3", b"")


class MockProvider(BaseProvider, Provider):
    """Test speech API provider."""

    def __init__(self, lang: str) -> None:
        """Initialize test provider."""
        super().__init__(lang)
        self.name = "Test"


class MockTTSEntity(BaseProvider, TextToSpeechEntity):
    """Test speech API provider."""

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return "Test"


class MockTTS(MockPlatform):
    """A mock TTS platform."""

    PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
        {vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES)}
    )

    def __init__(self, provider: MockProvider, **kwargs: Any) -> None:
        """Initialize."""
        super().__init__(**kwargs)
        self._provider = provider

    async def async_get_engine(
        self,
        hass: HomeAssistant,
        config: ConfigType,
        discovery_info: DiscoveryInfoType | None = None,
    ) -> Provider | None:
        """Set up a mock speech component."""
        return self._provider
