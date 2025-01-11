# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx

from fr24.authentication import login
from fr24.json import flight_list, flight_list_df, FlightListRequest

import pandas as pd

async def my_list() -> pd.DataFrame:
    async with httpx.AsyncClient() as client:
        auth = await login(client)
        if auth is not None:
            print(auth["message"])
        response = await flight_list(
            client,
            FlightListRequest(
                flight="AF291",
                timestamp="2024-04-01",  # (1)!
            ),
            auth=auth,
        )
        response.raise_for_status()
        list_ = response.json()
        return list_


list_ = await my_list()
df = flight_list_df(list_)
df
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:df0]
   flight_id number callsign   icao24 registration typecode origin destination           status                      STOD ETOD                      ATOD                      STOA                      ETOA                      ATOA
0        NaN  AF291     None      NaN         None      77W   RJBB        LFPG        Scheduled 2024-04-08 02:30:00+00:00  NaT                       NaT 2024-04-08 17:25:00+00:00                       NaT                       NaT
1        NaN  AF291     None      NaN         None      772   RJBB        LFPG        Scheduled 2024-04-07 02:30:00+00:00  NaT                       NaT 2024-04-07 17:25:00+00:00                       NaT                       NaT
2        NaN  AF291     None      NaN         None      772   RJBB        LFPG        Scheduled 2024-04-06 02:30:00+00:00  NaT                       NaT 2024-04-06 17:25:00+00:00                       NaT                       NaT
3        NaN  AF291     None      NaN         None      772   RJBB        LFPG        Scheduled 2024-04-05 02:30:00+00:00  NaT                       NaT 2024-04-05 17:25:00+00:00                       NaT                       NaT
4        NaN  AF291     None      NaN         None      77W   RJBB        LFPG        Scheduled 2024-04-03 02:30:00+00:00  NaT                       NaT 2024-04-03 17:25:00+00:00                       NaT                       NaT
5  882273605  AF291   AFR291  3754464       F-GSPA     B772   RJBB        LFPG  Estimated 19:06 2024-04-01 02:30:00+00:00  NaT 2024-04-01 02:56:21+00:00 2024-04-01 17:25:00+00:00 2024-04-01 17:06:08+00:00                       NaT
6  882083240  AF291   AFR291  3754478       F-GSPO     B772   RJBB        LFPG     Landed 19:15 2024-03-31 02:30:00+00:00  NaT 2024-03-31 02:47:05+00:00 2024-03-31 17:25:00+00:00                       NaT 2024-03-31 17:15:33+00:00
7  881882655  AF291   AFR291  3754467       F-GSPD     B772   RJBB        LFPG     Landed 18:47 2024-03-30 02:55:00+00:00  NaT 2024-03-30 03:27:31+00:00 2024-03-30 17:50:00+00:00                       NaT 2024-03-30 17:47:52+00:00
8  881661169  AF291   AFR291  3754470       F-GSPG     B772   RJBB        LFPG     Landed 19:14 2024-03-29 03:25:00+00:00  NaT 2024-03-29 03:41:26+00:00 2024-03-29 18:20:00+00:00                       NaT 2024-03-29 18:14:54+00:00
9  881224971  AF291   AFR291  3754487       F-GSPX     B772   RJBB        LFPG     Landed 22:22 2024-03-27 03:25:00+00:00  NaT 2024-03-27 06:58:33+00:00 2024-03-27 18:20:00+00:00                       NaT 2024-03-27 21:22:08+00:00
# --8<-- [end:df0]
"""
