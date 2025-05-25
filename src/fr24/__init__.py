from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from .authentication import login
from .cache import FR24Cache
from .configuration import FP_CONFIG_FILE, PATH_CONFIG
from .service import ServiceFactory

if TYPE_CHECKING:
    from typing import Any, Literal

    from typing_extensions import Self

    from .types.authentication import (
        Authentication,
        TokenSubscriptionKey,
        UsernamePassword,
    )


class FR24:
    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        """
        See docs [quickstart](../usage/quickstart.md#initialisation).

        :param client: The `httpx` client to use. If not provided, a
            new one will be created with HTTP/2 enabled by default. It is
            highly recommended to use `http2=True` to avoid
            [464 errors](https://github.com/cathaypacific8747/fr24/issues/23#issuecomment-2125624974)
            and to be consistent with the browser.
        """
        self.http = HTTPClient(
            httpx.AsyncClient(http2=True) if client is None else client
        )
        """The HTTP client for use in requests"""

        factory = ServiceFactory(self.http)
        # json
        self.flight_list = factory.build_flight_list()
        """Flight list service."""
        self.playback = factory.build_playback()
        """Playback service."""
        # gRPC
        self.live_feed = factory.build_live_feed()
        """Live feed service."""
        self.live_feed_playback = factory.build_live_feed_playback()
        """Live feed playback service."""
        self.nearest_flights = factory.build_nearest_flights()
        """Nearest flights service."""

    async def login(
        self,
        creds: (
            TokenSubscriptionKey | UsernamePassword | None | Literal["from_env"]
        ) = "from_env",
    ) -> None:
        """
        :param creds: Reads credentials from the environment variables or the
            config file if `creds` is set to `"from_env"` (default). Otherwise,
            provide the credentials directly.
        """
        await self.http._login(creds)

    async def __aenter__(self) -> Self:
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.__aexit__(*args)


class HTTPClient:
    """An HTTPX client for making requests to the API."""

    def __init__(
        self, client: httpx.AsyncClient, auth: Authentication | None = None
    ):
        self.client = client
        self.auth = auth

    async def _login(
        self,
        creds: (
            TokenSubscriptionKey | UsernamePassword | Literal["from_env"] | None
        ) = "from_env",
    ) -> None:
        self.auth = await login(self.client, creds)

    async def __aenter__(self) -> HTTPClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self.client is not None:
            await self.client.aclose()


__all__ = [
    "FP_CONFIG_FILE",
    "FR24",
    "PATH_CACHE",
    "PATH_CONFIG",
    "FR24Cache",
    "HTTPClient",
]
