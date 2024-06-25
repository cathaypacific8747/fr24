# ruff: noqa
# fmt: off
# %%
# --8<-- [start:script0]
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
            flight_id="35d692b1",
            timestamp=1719273600,
            auth=auth,
        )
        return list_


list_ = await my_playback()
df = playback_df(list_)
df
# --8<-- [end:script0]
# %%
"""
# --8<-- [start:df0]
                    timestamp   latitude   longitude  altitude  ground_speed  vertical_speed  track  squawk   ems  
0   2024-06-25 00:34:31+00:00  25.083984  121.251160         0             3               0    137       0  None   
1   2024-06-25 00:35:17+00:00  25.083664  121.251465         0             9               0    137       0  None   
2   2024-06-25 00:35:27+00:00  25.083344  121.251770         0             9               0    140       0  None   
3   2024-06-25 00:35:34+00:00  25.083101  121.251816         0             7               0    163       0  None   
4   2024-06-25 00:35:47+00:00  25.082882  121.251541         0             5               0    216       0  None   
..                        ...        ...         ...       ...           ...             ...    ...     ...   ...   
413 2024-06-25 02:08:13+00:00  22.312042  113.929344         0             5               0     39    1459  None   
414 2024-06-25 02:08:21+00:00  22.312243  113.929344         0             6               0     14    1459  None   
415 2024-06-25 02:08:30+00:00  22.312475  113.929214         0             6               0    345    1459  None   
416 2024-06-25 02:08:39+00:00  22.312706  113.929108         0             5               0    340    1459  None   
417 2024-06-25 02:08:53+00:00  22.312906  113.929039         0             3               0    340    1459  None   

[418 rows x 9 columns]
# --8<-- [end:df0]
"""
