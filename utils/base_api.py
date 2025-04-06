"""Base class for the API."""

from httpx import AsyncClient


class BaseApi:
    """Base class for the API."""

    def __init__(self):
        """Initialize ChatApi."""
        self._api_key: str = ""
        self._is_tor: bool = False
        self._is_browser: bool = False
        self._client: AsyncClient = AsyncClient()

    def with_api_key(self, api_key: str):
        """With api key."""
        self._api_key = api_key
        return self

    def use_tor(self):
        """Use tor."""
        self._is_tor = True

        # set up socks proxy
        self._client = AsyncClient(proxy="socks5://127.0.0.1:9050")
        return self

    def as_browser(self):
        """As browser."""
        self._is_browser = True
        return self
