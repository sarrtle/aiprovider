"""Streaming response model."""

from typing import Literal
from pydantic import BaseModel, model_validator


class StreamResponse(BaseModel):
    """Streaming response model."""

    id: str
    object: Literal["chat.completion.chunk"]
    created: int
    model: str
    choices: list["StreamResponseChoice"]
    usage: "StreamResponseUsage | None" = None


class StreamResponseUsage(BaseModel):
    """Usage model."""

    prompt_tokens: int
    total_tokens: int
    completion_tokens: int
    estimated_cost: float


class StreamResponseChoice(BaseModel):
    """Choice model."""

    index: int
    delta: "StreamResponseDelta"
    finish_reason: Literal["stop"] | None = None


class StreamResponseDelta(BaseModel):
    """Delta model."""

    role: Literal["assistant"]
    content: str
    tool_calls: list["StreamResponseToolCall"] | None = None
    logprobs: float | None = None

    @model_validator(mode="before")
    def _validate_empty_delta(cls, values: dict[str, object]):
        if "content" not in values:
            values["content"] = ""
        if "role" not in values:
            values["role"] = "assistant"
        return values


class StreamResponseToolCall(BaseModel):
    """Tool call model."""

    id: str
    function: "StreamResponseFunction"
    type: Literal["function"]


class StreamResponseFunction(BaseModel):
    """Function model."""

    name: str
    arguments: dict[str, object]
