"""Main application."""

import asyncio

from chat.chat_api import ChatApi
from chat.chat_builder import ChatBuilder

from models.vision.deepinfra.meta_llama import LLAMA4_MAVERICK_17B_128E_INSTRUCT_FP8

# from models.tts.deepinfra.kokoro import KOKORO
# from models.tts.deepinfra.canopylabs import ORPHEUS_3B
from models.tts.deepinfra.sesame import SESAME
from tts.tts_api import TTSApi
from utils.common import (
    convert_file_to_base64,
    save_tts_to_file,
)


async def test_chat():
    """Test  chat."""
    chat_api = ChatApi().use_tor().as_browser()

    # use with api key
    # chat_api = ChatApi().with_api_key("YOUR_API_KEY")

    chat = ChatBuilder(model=LLAMA4_MAVERICK_17B_128E_INSTRUCT_FP8)

    chat.add_system_message("You are a helpful assistant.")

    image = await convert_file_to_base64("test.png")

    chat.add_user_message(
        "what are the clickable elements on this image. Can you put them in a list on this format [{'text': name-of-element, 'coords': [x1, y1, x2, y2]}, {and so on}] without explanation and they should be in floats like 0.532...",
        image_as_base64=image,
    )

    response = await chat_api.send_chat(chat)
    print(response.choices[0].message.content)


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
