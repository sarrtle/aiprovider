"""Main application."""

import asyncio
from chat.chat_api import ChatApi
from chat.chat_builder import ChatBuilder

from models.text_generation.deepinfra.meta_llama import LLAMA3_1_8B_INSTRUCT_TURBO


async def main():
    """Application."""
    chat_api = ChatApi().use_tor().as_browser()

    # use with api key
    # chat_api = ChatApi().with_api_key("YOUR_API_KEY")

    chat = ChatBuilder(model=LLAMA3_1_8B_INSTRUCT_TURBO)

    chat.add_system_message("You are a helpful assistant.")
    chat.add_user_message("Hi, what can you do")

    async for stream_response in chat_api.send_chat_stream(chat=chat):
        print(stream_response.choices[0].delta.content)


if __name__ == "__main__":
    asyncio.run(main())
