"""Chat api."""

from collections.abc import AsyncGenerator
from httpx import AsyncClient

from chat.chat_builder import ChatBuilder
from chat.schemas.normal_response import NormalResponse
from chat.schemas.stream_response import StreamResponse

import json


class ChatApi:
    """ChatApi class."""

    def __init__(self):
        """Initialize ChatApi."""
        self._api_key: str = ""
        self._is_tor: bool = False
        self._is_browser: bool = False
        self._client: AsyncClient = AsyncClient()

    def with_api_key(self, api_key: str) -> "ChatApi":
        """With api key."""
        self._api_key = api_key
        return self

    def use_tor(self) -> "ChatApi":
        """Use tor."""
        self._is_tor = True

        # set up socks proxy
        self._client = AsyncClient(proxy="socks5://127.0.0.1:9050")
        return self

    def as_browser(self) -> "ChatApi":
        """As browser."""
        self._is_browser = True
        return self

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
            headers = self._get_browser_headers()

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
            headers = self._get_browser_headers()

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

    def _get_browser_headers(self):
        return {
            "Content-Type": "application/json",
            "Host": "api.deepinfra.com",
            "Origin": "https://deepinfra.com",
            "Pragma": "no-cache",
            "Referer": "https://deepinfra.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36",
            "Priority": "u=0",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "X-Deepinfra-Source": "model-embed",
        }
