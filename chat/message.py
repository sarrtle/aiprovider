"""Message object."""

from typing import Literal
from pydantic import BaseModel


class ImageUrl(BaseModel):
    """Image url."""

    url: str


class ImageContent(BaseModel):
    """Image content."""

    image_url: ImageUrl
    type: Literal["image_url"]


class TextContent(BaseModel):
    """Text content."""

    text: str
    type: Literal["text"]


class Message(BaseModel):
    """Message class."""

    role: Literal["user", "assistant", "system"]
    content: str | list[ImageContent | TextContent]
