"""Base response object simplified."""

from typing import Literal
from chat.schemas.normal_response import NormalResponseToolCall
from chat.schemas.stream_response import StreamResponseToolCall
from chat.tool import Tool


class ChatResponse:
    """Chat response simplified."""

    def __init__(
        self,
        content: str,
        role: Literal["assistant", "tool_call"],
        name: str,
        tool_calls: list[NormalResponseToolCall] | list[StreamResponseToolCall],
    ):
        """Initialize ChatResponse.

        Args:
            content: The content of the message.
            role: The role of the message.
            name: The name of the message.
            tool_calls: The tool calls of the message.

        """
        self._message: str = content
        self._role: Literal["assistant", "tool_call"] = role
        self._name: str | None = name
        self._tool_calls: (
            list[NormalResponseToolCall] | list[StreamResponseToolCall]
        ) = tool_calls

    @property
    def content(self) -> str:
        """Content."""
        return self._message

    @property
    def role(self) -> Literal["assistant", "tool_call"]:
        """Role."""
        return self._role

    @property
    def name(self) -> str | None:
        """Name."""
        return self._name

    def is_tool_call(self) -> bool:
        """Check if response is a tool call."""
        return bool(self._tool_calls)

    def get_tool_calls(self, tools: dict[str, Tool]) -> list[Tool]:
        """Get tool calls.

        Ready to run functions. Invoking by `tool.run()`

        Args:
            tools: list of tools to use.

        """
        # parse tool calls into ToolCall objects
        to_return = [
            tools[tool_name].register(tool_call.function.arguments, tool_call.id)
            for tool_name in tools
            for tool_call in self._tool_calls
        ]

        return to_return
