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


async def my_track() -> pd.DataFrame:
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


list_ = await my_track()  # type: ignore
df = playback_df(list_)
df

# %%
