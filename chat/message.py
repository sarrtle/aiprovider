"""Message object."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Message:
    """Message class."""

    role: Literal["user", "assistant", "system"]
    content: str
