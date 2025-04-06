"""TTS normal response."""

from pydantic import BaseModel

from typing import Literal


class TTSNormalResponse(BaseModel):
    """TTS normal response model."""

    input_character_length: int
    output_format: Literal["mp3", "opus", "flac", "wav", "pcm"] = "opus"
    audio: str  # base64
