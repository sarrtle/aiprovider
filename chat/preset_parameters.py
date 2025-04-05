"""Preset parameters."""

from enum import Enum


CHAT = {"temperature": 0.7, "top_p": 0.9}

CODING = {
    "temperature": 0.2,
    "top_p": 1,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.2,
}

CREATIVE_STORY_TELLING = {
    "temperature": 1.2,
    "top_p": 1.0,
    "frequency_penalty": 1.2,
    "presence_penalty": 0.5,
}


class PresetParameters(Enum):
    """Preset parameters."""

    CHAT = CHAT
    CODING = CODING
    CREATIVE_STORY_TELLING = CREATIVE_STORY_TELLING
