from __future__ import annotations

import asyncio
import configparser
import json
import logging
import os
from pathlib import Path

import httpx
from appdirs import user_config_dir

from .common import DEFAULT_HEADERS
from .types.fr24 import Authentication

username = os.environ.get("fr24_username", None)
password = os.environ.get("fr24_password", None)
subscription_key = os.environ.get("fr24_subscription_key", None)
token = os.environ.get("fr24_token", None)

if (config_file := (Path(user_config_dir("fr24")) / "fr24.conf")).exists():
    config = configparser.ConfigParser()
    config.read(config_file.as_posix())

    username = config.get("global", "username", fallback=None)
    password = config.get("global", "password", fallback=None)
    subscription_key = config.get("global", "subscription_key", fallback=None)
    token = config.get("global", "token", fallback=None)


_log = logging.getLogger()


async def login(client: httpx.AsyncClient) -> None | Authentication:
    if username is None or password is None:
        if subscription_key is None:
            return None
        return {
            "userData": {
                "subscriptionKey": subscription_key,
                "accessToken": token,
            },
            "message": "using subscriptionKey and/or accessToken.",
        }

    res = await client.post(
        "https://www.flightradar24.com/user/login",
        data={"email": username, "password": password},
        headers=DEFAULT_HEADERS,
    )
    res.raise_for_status()
    return res.json()  # type: ignore
    # json['userData']['accessToken']  => Bearer
    # json['userData']['subscriptionKey']  => token


async def async_main() -> None:
    async with httpx.AsyncClient() as client:
        auth = await login(client)
        if auth is None:
            _log.warning(
                "Provide credentials in environment variables: either "
                "fr24_username + fr24_password or "
                "fr24_subscription_key + fr24_token (optional)"
            )
        else:
            print(f"Login successful: {json.dumps(auth, indent=2)}")


def main() -> None:
    asyncio.run(async_main())
