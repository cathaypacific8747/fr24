from __future__ import annotations

import logging
from dataclasses import dataclass
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


def intercept_logs_with_loguru(
    level: logging._Level = logging.INFO, modules: tuple[str, ...] = ()
) -> None:
    """
    Intercepts stdlib logging to stderr with loguru.

    :param level: The stdlib logging level to intercept.
    :param modules: The modules to intercept.
    """
    import inspect
    from itertools import chain

    from loguru import logger

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level if it exists.
            try:
                level: str | int = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message.
            frame, depth = inspect.currentframe(), 0
            while frame:
                filename = frame.f_code.co_filename
                is_logging = filename == logging.__file__
                is_frozen = "importlib" in filename and "_bootstrap" in filename
                if depth > 0 and not (is_logging or is_frozen):
                    break
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=level, force=True)
    for logger_name in chain(("",), modules):
        logger_module = logging.getLogger(logger_name)
        logger_module.handlers = [InterceptHandler(level=level)]
        logger_module.propagate = False


__all__ = [
    "FP_CONFIG_FILE",
    "FR24",
    "PATH_CACHE",
    "PATH_CONFIG",
    "FR24Cache",
    "HTTPClient",
]
