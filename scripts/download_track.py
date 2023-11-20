# %%
from fr24.history import flight_list, flight_list_df
from fr24.authentication import login

import httpx
import pandas as pd


async def my_list() -> pd.DataFrame:
    async with httpx.AsyncClient() as client:
        auth = await login(client)
        if auth is not None:
            print(auth["message"])
        list_ = await flight_list(
            client,
            flight="AF291",
            timestamp="2023-09-06",
            limit=5,
            auth=auth,
        )
        return flight_list_df(list_)


df = await my_list()
df

# %%
from fr24.history import playback, playback_df
from fr24.authentication import login

import httpx
import pandas as pd


async def my_track() -> pd.DataFrame:
    async with httpx.AsyncClient() as client:
        auth = await login(client)
        if auth is not None:
            print(auth["message"])
        list_ = await playback(
            client,
            flight_id="31e42151",
            timestamp="2023-09-05",
            auth=auth,
        )
        return playback_df(list_)


df = await my_track()
df

# %%
