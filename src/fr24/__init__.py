from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
from appdirs import user_cache_dir, user_config_dir

from .authentication import login
from .service import ServiceFactory

if TYPE_CHECKING:
    from typing import Any, Literal

    from typing_extensions import Self

    from .types.authentication import (
        Authentication,
        TokenSubscriptionKey,
        UsernamePassword,
    )


PATH_CACHE = Path(user_cache_dir("fr24"))
if cache_path := os.environ.get("XDG_CACHE_HOME"):
    PATH_CACHE = Path(cache_path) / "fr24"

PATH_CONFIG = Path(user_config_dir("fr24"))
if config_path := os.environ.get("XDG_CONFIG_HOME"):
    PATH_CONFIG = Path(config_path) / "fr24"

FP_CONFIG_FILE = PATH_CONFIG / "fr24.conf"


class FR24:
    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        *,
        base_dir: Path | str = PATH_CACHE,
    ) -> None:
        """
        See docs [quickstart](../usage/quickstart.md#initialisation).

        :param client: The `httpx` client to use. If not provided, a
            new one will be created with HTTP/2 enabled by default. It is
            highly recommended to use `http2=True` to avoid
            [464 errors](https://github.com/cathaypacific8747/fr24/issues/23#issuecomment-2125624974)
            and to be consistent with the browser.
        :param base_dir:
            See [cache directory](../usage/cli.md#directories).
        """
        self.http = HTTPClient(
            httpx.AsyncClient(http2=True) if client is None else client
        )
        """The HTTP client for use in requests"""
        self.__base_dir = Path(base_dir)

        factory = ServiceFactory(self.http, self.base_dir)
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

    @property
    def base_dir(self) -> Path:
        """The [cache directory](../usage/cli.md#directories)."""
        return self.__base_dir

    async def __aenter__(self) -> Self:
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.__aexit__(*args)


@dataclass
class HTTPClient:
    """An HTTPX client for making requests to the API."""

    client: httpx.AsyncClient
    auth: Authentication | None = None

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
