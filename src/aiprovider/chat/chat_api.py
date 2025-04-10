"""Chat api."""

from collections.abc import AsyncGenerator

from aiprovider.chat.chat_builder import ChatBuilder
from aiprovider.chat.response import ChatResponse
from aiprovider.chat.schemas.normal_response import NormalResponse
from aiprovider.chat.schemas.stream_response import StreamResponse

import json

from aiprovider.utils.base_api import BaseApi
from aiprovider.utils.common import get_deepinfra_browser_headers


class ChatApi(BaseApi):
    """ChatApi class."""

    def __init__(self):
        """Initialize ChatApi."""
        super().__init__()

    async def send_chat(self, chat: ChatBuilder) -> ChatResponse:
        """Send chat."""
        # construct payload
        payload: dict[str, object] = {
            "model": chat.model,
            "messages": [
                message.model_dump(exclude_none=True) for message in chat.messages
            ],
            "tools": chat.tools,
            "tool_choice": chat.tool_choice,
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
            url, headers=headers, json=payload, timeout=300
        )

        try:
            normal_response: NormalResponse = NormalResponse.model_validate(
                response.json()
            )
        except ValueError:
            raise ValueError(
                "Could not parse response: {}", json.dumps(response.json(), indent=4)
            )

        return ChatResponse(
            content=normal_response.choices[0].message.content,
            role=normal_response.choices[0].message.role,
            name=normal_response.choices[0].message.name or "",
            tool_calls=normal_response.choices[0].message.tool_calls or [],
        )

    async def send_chat_stream(self, chat: ChatBuilder) -> AsyncGenerator[ChatResponse]:
        """Send chat as stream."""
        # construct payload
        payload: dict[str, object] = {
            "model": chat.model,
            "messages": [
                message.model_dump(exclude_none=True) for message in chat.messages
            ],
            "tools": chat.tools,
            "tool_choice": chat.tool_choice,
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

                    try:
                        stream_response = StreamResponse.model_validate(
                            json.loads(str_data)
                        )
                    except ValueError:
                        raise ValueError(
                            "Could not parse response: {}",
                            json.dumps(json.loads(str_data), indent=4),
                        )

                    # parse stream response to real object
                    yield ChatResponse(
                        content=stream_response.choices[0].delta.content,
                        role=stream_response.choices[0].delta.role,
                        name=stream_response.choices[0].delta.name or "",
                        tool_calls=stream_response.choices[0].delta.tool_calls or [],
                    )
