"""Normal response model."""

import json
from pydantic import BaseModel, model_validator
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
    finish_reason: Literal["stop", "tool_calls"] | None = None


class NormalResponseMessage(BaseModel):
    """Message model."""

    role: Literal["assistant"]
    content: str = ""
    name: str | None = None
    tool_calls: list["NormalResponseToolCall"] | None = None

    @model_validator(mode="before")
    def _content_should_not_be_null(cls, values: dict[str, object]):
        if values["content"] is None:
            values["content"] = ""
        return values


class NormalResponseToolCall(BaseModel):
    """Tool call model."""

    id: str
    type: Literal["function"]
    function: "NormalResponseFunction"


class NormalResponseFunction(BaseModel):
    """Function model."""

    name: str
    arguments: dict[str, object]

    @model_validator(mode="before")
    def _validate_function_arguents(cls, values: dict[str, str]):
        if "arguments" not in values:
            values["arguments"] = "{}"

        values["arguments"] = json.loads(values["arguments"])
        return values


class NormalResponseUsage(BaseModel):
    """Usage model."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float
