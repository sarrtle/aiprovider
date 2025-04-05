"""Chat api."""

from httpx import AsyncClient

from chat.chat_builder import ChatBuilder


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

    async def send_chat(self, chat: ChatBuilder, as_stream: bool = False):
        """Send chat."""
        # construct payload
        payload: dict[str, object] = {
            "model": chat.model,
            "messages": [message.__dict__ for message in chat.messages],
        }
        for param_key, param_value in chat.parameters.value.items():
            payload[param_key] = param_value

        # add strem or not
        payload["stream"] = as_stream

        # set up headers
        headers: dict[str, str] = {}

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
        if as_stream:
            async with self._client.stream(
                "POST",
                url,
                headers=headers,
                json=payload,
            ) as response:
                async for chunk in response.aiter_text():
                    print(chunk)
                    print("---")
            pass
        else:
            response = await self._client.post(
                url,
                headers=headers,
                json=payload,
            )

            print(response.json())

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
