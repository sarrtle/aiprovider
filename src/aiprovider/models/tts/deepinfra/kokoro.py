"""Kokoro models."""

from enum import Enum


KOKORO: str = "hexgrad/Kokoro-82M"


class KokoroVoices(Enum):
    """Kokoro voices."""

    AF_BELLA = "af_bella"
    AF_HEART = "af_heart"

    AM_FENRIR = "am_fenrir"
    AM_LIAM = "am_liam"
    AM_ONYX = "am_onyx"
