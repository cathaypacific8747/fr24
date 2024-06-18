from __future__ import annotations

import base64
import configparser
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import httpx
from appdirs import user_config_dir
from loguru import logger

from .common import DEFAULT_HEADERS
from .types.fr24 import Authentication, TokenSubscriptionKey, UsernamePassword


def get_credentials() -> TokenSubscriptionKey | UsernamePassword | None:
    """
    Reads credentials from the environment variables, overriding it with
    the config file if it exists.
    """
    username = os.environ.get("fr24_username", None)
    password = os.environ.get("fr24_password", None)
    subscription_key = os.environ.get("fr24_subscription_key", None)
    token = os.environ.get("fr24_token", None)

    if (config_file := (Path(user_config_dir("fr24")) / "fr24.conf")).exists():
        config = configparser.ConfigParser()
        config.read(config_file.as_posix())

        username = config.get("global", "username", fallback=None)
        password = config.get("global", "password", fallback=None)
        subscription_key = config.get(
            "global", "subscription_key", fallback=None
        )
        token = config.get("global", "token", fallback=None)

    if username and password:
        return {"username": username, "password": password}
    if subscription_key and token:
        return {"subscriptionKey": subscription_key, "token": token}
    return None


async def login(
    client: httpx.AsyncClient,
    creds: (
        TokenSubscriptionKey | UsernamePassword | None | Literal["from_env"]
    ) = "from_env",
) -> None | Authentication:
    """
    Read credentials and logs into the API.

    By default, credentials are read from the environment variables or the
    config file if `creds_override` is not set. Then, if the credentials:
    - `username` and `password` is set: makes a POST request to the login
    endpoint
    - `subscription_key` and `token` is set: returns immediately
    - otherwise, `None` is returned
    """
    creds = get_credentials() if creds == "from_env" else creds

    if creds is None:
        return None
    if (u := creds.get("username")) and (p := creds.get("password")):
        return await login_with_username_password(client, u, p)  # type: ignore[arg-type]
    if s := creds.get("subscriptionKey"):
        t = creds.get("token")
        return await login_with_token_subscription_key(client, s, t)  # type: ignore[arg-type]

    logger.warning(
        "Expected username+password or subscriptionKey+Optional[token] pair,"
        "but one or both are missing. Falling back to anonymous access."
    )
    return None


async def login_with_username_password(
    client: httpx.AsyncClient,
    username: str,
    password: str,
) -> Authentication:
    """
    Retrieve bearer token and subscription key from the API.

    Bearer: `json['userData']['accessToken']`
    `token=` query param: `json['userData']['subscriptionKey']`
    """
    res = await client.post(
        "https://www.flightradar24.com/user/login",
        data={"email": username, "password": password},
        headers=DEFAULT_HEADERS,
    )
    res.raise_for_status()
    return res.json()  # type: ignore


async def login_with_token_subscription_key(
    _client: httpx.AsyncClient,
    subscription_key: str,
    token: str | None,
) -> Authentication | None:
    """
    Login with subscription key and/or token.
    Falls back to anonymous access if token is expired or invalid.
    """
    if token is None:
        return {
            "userData": {
                "subscriptionKey": subscription_key,
            },
            "message": "using environment `subscription_key`",
        }

    try:
        payload = json.loads(base64.b64decode(token.split(".")[1]))
    except Exception as e:
        logger.error(
            f"Failed to parse token: {e}. Falling back to anonymous access"
        )
        return None

    if time.time() > (exp := payload["exp"]):
        exp_f = datetime.fromtimestamp(exp, timezone.utc).isoformat()
        logger.error(
            f"Token has expired at {exp_f}. Falling back to anonymous access"
        )
        return None

    return {
        "user": {
            "id": payload.get("userId"),
        },
        "userData": {
            "subscriptionKey": subscription_key,
            "accessToken": token,
            "dateExpires": exp,
        },
        "message": "using environment `subscription_key` and `access_token`",
    }
