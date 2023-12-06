# ruff: noqa: F704, F811, E402
# %%
import httpx
from fr24.authentication import login
from fr24.history import flight_list, flight_list_df

import pandas as pd


async def my_list() -> pd.DataFrame:
    async with httpx.AsyncClient() as client:
        auth = await login(client)
        if auth is not None:
            print(auth["message"])
        list_ = await flight_list(
            client,
            flight="AF291",
            timestamp="2023-11-20",
            auth=auth,
        )
        return flight_list_df(list_)


df = await my_list()  # type: ignore
df

# %%
import httpx
from fr24.authentication import login
from fr24.history import playback, playback_df

import pandas as pd


async def my_playback() -> pd.DataFrame:
    async with httpx.AsyncClient() as client:
        auth = await login(client)
        if auth is not None:
            print(auth["message"])
        list_ = await playback(
            client,
            flight_id="32ddcf4e",
            timestamp=1700191500,
            auth=auth,
        )
        return list_


list_ = await my_playback()  # type: ignore
df = playback_df(list_)
df

# %%

import httpx
from fr24.history import airport_list
from fr24.types.fr24 import AirportList

import pandas as pd


async def my_arrivals() -> AirportList:
    async with httpx.AsyncClient() as client:
        list_ = await airport_list(
            client,
            airport="tls",
            mode="arrivals",
        )
        return list_


airports = await my_arrivals()  # type: ignore

# %%
from fr24.find import find
from fr24.types.find import FindResult


async def my_find() -> FindResult:
    results = await find("paris")
    assert results is not None
    return results


results = await my_find()  # type: ignore
# %%
import asyncio

import httpx
from fr24.authentication import login
from fr24.core import FR24
from fr24.history import flight_list_df
from loguru import logger

import pandas as pd


async def my_full_list() -> None:
    async with FR24() as fr24:
        if fr24.auth is not None:
            logger.info(fr24.auth["message"])
        for reg in ["B-KJA", "B-KJB", "B-KJC", "B-KJD"]:
            logger.info(f"Updating {reg}")
            await fr24.flight_list_cache_update(reg=reg)
            await asyncio.sleep(2)


await my_full_list()  # type: ignore

# %%
