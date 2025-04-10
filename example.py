"""Main application."""

import asyncio
from typing import Literal

from aiprovider import ChatApi, ChatBuilder
from aiprovider.models.text_generation.deepinfra.meta_llama import (
    LLAMA3_1_70B_INSTRUCT_TURBO,
)
from aiprovider import TTSApi
from aiprovider import save_tts_to_file
from aiprovider.models.tts.deepinfra.sesame import SESAME

# from models.tts.deepinfra.kokoro import KOKORO
# from models.tts.deepinfra.canopylabs import ORPHEUS_3B


def get_weather(city: str, unit: Literal["celsius", "fahrenheit"]) -> dict[str, str]:
    """Get the weather of a city.

    Use Api to get the weather of chosen place.

    Args:
        city: The city to get the weather of.
        unit: The unit to return the weather in.

    Returns:
        The weather of the city.

    """
    return {"city": city, "unit": unit, "weather": "20 degrees"}


async def test_chat():
    """Test chat."""
    chat_api = ChatApi().use_tor().as_browser()

    # use with api key
    # chat_api = ChatApi().with_api_key("API-KEY")

    chat = ChatBuilder(model=LLAMA3_1_70B_INSTRUCT_TURBO)

    chat.add_system_message("You are a helpful assistant.")
    while True:
        try:
            chat.add_user_message(
                input("User: "),
            )

            response = await chat_api.send_chat(chat)
            print("Bot: ", response.content)
        except KeyboardInterrupt:
            break


async def test_tts():
    """Test tts."""
    tts_api = TTSApi().use_tor().as_browser()

    # use with api key
    # tts_api = TTSApi().with_api_key("YOUR_API_KEY")

    response = await tts_api.send_tts_with_clone_audio(
        "Hmm. But what are you doing here in the first place?",
        SESAME,
        "test-input.ogg",
        "Your text audio transcription",
    )

    await save_tts_to_file(response.audio, "test.ogg")


async def main():
    """Application."""
    await test_chat()
    # await test_tts()


if __name__ == "__main__":
    asyncio.run(main())
