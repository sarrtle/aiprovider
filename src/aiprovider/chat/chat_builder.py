"""Handles and builds chat messages."""

from typing import Literal
from aiprovider.chat.message import ImageContent, ImageUrl, Message, TextContent
from aiprovider.chat.preset_parameters import PresetParameters
from aiprovider.chat.tool import Tool


class ChatBuilder:
    """ChatBuilder class."""

    def __init__(self, model: str, tool_only: bool = False):
        """Initialize ChatBuilder.

        Args:
            model: The model to use.
            tool_only: Whether to only use tools.

        """
        self.model: str = model
        self.tool_only: bool = tool_only
        self.messages: list[Message] = []
        self.tools: list[dict[str, object]] = []
        self.tool_choice: Literal["auto", "none"] = "auto"
        self.parameters: PresetParameters = PresetParameters.CHAT

    def add_user_message(self, message: str, image_as_base64: str | None = None):
        """Add user message.

        Args:
            message: The message to add.
            image_as_base64: The image to add as base64.

        """
        if image_as_base64 is not None:

            # add images as ImageContent

            self.messages.append(
                Message(
                    role="user",
                    content=[
                        ImageContent(
                            image_url=ImageUrl(url=image_as_base64), type="image_url"
                        ),
                        TextContent(text=message, type="text"),
                    ],
                )
            )
        else:
            self.messages.append(Message(role="user", content=message))

    def add_assistant_message(self, message: str):
        """Add assistant message.

        Args:
            message: The message to add.

        """
        self.messages.append(Message(role="assistant", content=message))

    def add_system_message(self, message: str):
        """Add system message.

        Args:
            message: The message to add.

        """
        self.messages.append(Message(role="system", content=message))

    def add_tool(self, tool: Tool):
        """Add function as a tool to call.

        Args:
            tool: The tool to add.

        Raises:
            RuntimeError: If `tool_only` is True and more than one tool is added.

        """
        # assuming it is the current provider for now.
        self.tools.append({"function": tool.generate_function_schema()})

    def add_tool_response(self, tool: Tool):
        """Add tool response."""
        self.messages.append(
            Message(
                role="tool",
                content=str(tool.function_response),
                tool_call_id=tool.tool_id,
            )
        )

    def set_parameters(self, parameters: PresetParameters):
        """Set parameters."""
        self.parameters = parameters

    def set_model(self, model: str):
        """Set model."""
        self.model = model
