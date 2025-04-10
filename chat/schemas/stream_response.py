"""Streaming response model."""

import json
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

    name: str | None = None
    # at stream, assistant is still the role even if it is calling a tool.
    role: Literal["assistant"] = "assistant"
    content: str = ""
    tool_calls: list["StreamResponseToolCall"] | None = None
    logprobs: float | None = None

    @model_validator(mode="before")
    def _role_should_not_be_null(cls, values: dict[str, object]):
        if "role" in values and values["role"] is None:
            values["role"] = "assistant"
        return values

    @model_validator(mode="before")
    def _content_should_not_be_null(cls, values: dict[str, object]):
        if "content" in values and values["content"] is None:
            values["content"] = ""
        return values


class StreamResponseToolCall(BaseModel):
    """Tool call model."""

    id: str
    type: Literal["function"]
    function: "StreamResponseFunction"


class StreamResponseFunction(BaseModel):
    """Function model."""

    name: str
    arguments: dict[str, object]

    @model_validator(mode="before")
    def _validate_function_arguents(cls, values: dict[str, str]):
        if "arguments" not in values:
            values["arguments"] = "{}"

        values["arguments"] = json.loads(values["arguments"])
        return values
