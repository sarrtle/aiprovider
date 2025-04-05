"""Handles and builds chat messages."""

from chat.message import Message
from chat.preset_parameters import PresetParameters


class ChatBuilder:
    """ChatBuilder class."""

    def __init__(self, model: str):
        """Initialize ChatBuilder."""
        self.model: str = model
        self.messages: list[Message] = []
        self.parameters: PresetParameters = PresetParameters.CHAT

    def add_user_message(self, message: str):
        """Add user message."""
        self.messages.append(Message("user", message))

    def add_assistant_message(self, message: str):
        """Add assistant message."""
        self.messages.append(Message("assistant", message))

    def add_system_message(self, message: str):
        """Add system message."""
        self.messages.append(Message("system", message))

    def set_parameters(self, parameters: PresetParameters):
        """Set parameters."""
        self.parameters = parameters

    def set_model(self, model: str):
        """Set model."""
        self.model = model
