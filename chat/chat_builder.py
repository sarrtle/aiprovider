"""Handles and builds chat messages."""

from chat.message import ImageContent, ImageUrl, Message, TextContent
from chat.preset_parameters import PresetParameters


class ChatBuilder:
    """ChatBuilder class."""

    def __init__(self, model: str):
        """Initialize ChatBuilder."""
        self.model: str = model
        self.messages: list[Message] = []
        self.parameters: PresetParameters = PresetParameters.CHAT

    def add_user_message(self, message: str, image_as_base64: str | None = None):
        """Add user message."""
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
        """Add assistant message."""
        self.messages.append(Message(role="assistant", content=message))

    def add_system_message(self, message: str):
        """Add system message."""
        self.messages.append(Message(role="system", content=message))

    def set_parameters(self, parameters: PresetParameters):
        """Set parameters."""
        self.parameters = parameters

    def set_model(self, model: str):
        """Set model."""
        self.model = model
