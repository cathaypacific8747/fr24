from __future__ import annotations

import configparser
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


async def login(client: httpx.AsyncClient) -> None | Authentication:
    """
    Create credentials for the user (if any). If the environment variables:

    - `subscription_key` and `token` is set: it returns the pair
    - `username` and `password` is set: it fetches the token and
    subscription key from the API
    - otherwise, it returns `None`
    """
    if username is None or password is None:
        if not subscription_key:
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
