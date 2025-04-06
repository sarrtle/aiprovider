"""Chat api."""

from collections.abc import AsyncGenerator

from chat.chat_builder import ChatBuilder
from chat.schemas.normal_response import NormalResponse
from chat.schemas.stream_response import StreamResponse

import json

from utils.base_api import BaseApi
from utils.common import get_deepinfra_browser_headers


class ChatApi(BaseApi):
    """ChatApi class."""

    def __init__(self):
        """Initialize ChatApi."""
        super().__init__()

    async def send_chat(self, chat: ChatBuilder) -> NormalResponse:
        """Send chat."""
        # construct payload
        payload: dict[str, object] = {
            "model": chat.model,
            "messages": [message.__dict__ for message in chat.messages],
        }
        for param_key, param_value in chat.parameters.value.items():
            payload[param_key] = param_value

        # set up headers
        headers: dict[str, str] = {"Connection": "keep-alive"}

        # if simulating browser
        if self._is_browser:
            # set httpx header
            headers = get_deepinfra_browser_headers()

        # with api keyss
        else:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }

        # send request

        url: str = "https://api.deepinfra.com/v1/openai/chat/completions"

        # streaming
        response = await self._client.post(
            url,
            headers=headers,
            json=payload,
        )

        return NormalResponse.model_validate(response.json())

    async def send_chat_stream(
        self, chat: ChatBuilder
    ) -> AsyncGenerator[StreamResponse]:
        """Send chat as stream."""
        # construct payload
        payload: dict[str, object] = {
            "model": chat.model,
            "messages": [message.__dict__ for message in chat.messages],
        }
        for param_key, param_value in chat.parameters.value.items():
            payload[param_key] = param_value

        # add strem or not
        payload["stream"] = True

        # set up headers
        headers: dict[str, str] = {"Connection": "keep-alive"}

        # if simulating browser
        if self._is_browser:
            # set httpx header
            headers = get_deepinfra_browser_headers()

        # with api keyss
        else:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }

        # send request
        url: str = "https://api.deepinfra.com/v1/openai/chat/completions"

        async with self._client.stream(
            "POST",
            url,
            headers=headers,
            json=payload,
        ) as response:
            async for chunk in response.aiter_text():
                # clean chunk
                chunk = chunk.strip()

                # split new lines because sometimes chunk consists
                # of many data: {}

                splitted_text = chunk.split("\n")

                # remove empty strings
                splitted_text = list(filter(None, splitted_text))

                for str_data in splitted_text:
                    if str_data == "data: [DONE]" or str_data.startswith(": ping"):
                        continue

                    # remove the data: {} prefix
                    str_data = str_data.strip("data: ")

                    stream_response = StreamResponse.model_validate(
                        json.loads(str_data)
                    )

                    yield stream_response
