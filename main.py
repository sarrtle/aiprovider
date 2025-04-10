"""Main application."""

import asyncio
from typing import Literal

from chat.chat_api import ChatApi
from chat.chat_builder import ChatBuilder

from chat.tool import Tool
from models.text_generation.deepinfra.meta_llama import (
    LLAMA3_1_70B_INSTRUCT_TURBO,
)

# from models.tts.deepinfra.kokoro import KOKORO
# from models.tts.deepinfra.canopylabs import ORPHEUS_3B
from models.tts.deepinfra.sesame import SESAME
from tts.tts_api import TTSApi
from utils.common import (
    save_tts_to_file,
)


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
    # chat_api = ChatApi().use_tor().as_browser()

    # use with api key
    chat_api = ChatApi().with_api_key("API-KEY")

    chat = ChatBuilder(model=LLAMA3_1_70B_INSTRUCT_TURBO)

    chat.add_system_message("You are a helpful assistant.")

    tool = Tool(get_weather)
    chat.add_tool(tool)

    tools = {tool.name: tool}

    while True:
        try:
            chat.add_user_message(
                input("User: "),
            )

            response = await chat_api.send_chat(chat)
            if response.is_tool_call():
                to_call = response.get_tool_calls(tools)
                print("calling tools:", [tn.name for tn in to_call])
                _ = await asyncio.gather(*[tool.run() for tool in to_call])
                for called_tools in to_call:
                    chat.add_tool_response(called_tools)

                response = await chat_api.send_chat(chat)

            print("Bot: ", response.content, response.is_tool_call())
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
        "Happy birthday! So, what are your plans for the day? Oh, why don't we celebrate on Watatsumi Island? First, I'll take you out at daybreak to see the sunrise, then we can go diving during the heat of the day. In the evening, we can go for a stroll around Sangonomiya Shrine. If it rains, we'll find somewhere cozy to hide out with a few strategy books, and try to bake a cake together! In any case, no need to plan anything, the grand strategist has everything thought out for you!",
    )

    await save_tts_to_file(response.audio, "test.ogg")


async def main():
    """Application."""
    await test_chat()
    # await test_tts()


if __name__ == "__main__":
    asyncio.run(main())
