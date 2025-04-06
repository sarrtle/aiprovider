"""Normal response model."""

from pydantic import BaseModel
from typing import Literal


class NormalResponse(BaseModel):
    """Normal response model."""

    id: str
    object: Literal["chat.completion"]
    created: int
    model: str
    choices: list["NormalResponseChoice"]
    usage: "NormalResponseUsage"


class NormalResponseChoice(BaseModel):
    """Choice model."""

    index: int
    message: "NormalResponseMessage"
    finish_reason: Literal["stop"] | None = None


class NormalResponseMessage(BaseModel):
    """Message model."""

    role: Literal["assistant"]
    content: str


class NormalResponseUsage(BaseModel):
    """Usage model."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float
