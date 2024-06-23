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
            flight_id="349685a9",
            timestamp=1711908900,
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
                    timestamp   latitude   longitude  altitude  ground_speed  vertical_speed  track  squawk
0   2024-04-01 03:48:45+00:00  23.293760  113.232841      5025           229            2880    209       0
1   2024-04-01 03:49:18+00:00  23.260664  113.218842      6575           241            1856    191       0
2   2024-04-01 03:49:23+00:00  23.253983  113.217407      6725           247            1472    191       0
3   2024-04-01 03:49:28+00:00  23.249258  113.216347      6825           252            1152    191       0
4   2024-04-01 03:49:30+00:00  23.246792  113.215790      6850           254             960    191       0
..                        ...        ...         ...       ...           ...             ...    ...     ...
338 2024-04-01 04:41:00+00:00  22.317202  113.926025         0            17               0     70    1618
339 2024-04-01 04:41:07+00:00  22.317387  113.926598         0            18               0     70    1618
340 2024-04-01 04:41:29+00:00  22.318027  113.928604         0             0               0     70    1618
341 2024-04-01 04:42:51+00:00  22.317478  113.930832         0             3               0    261    1618
342 2024-04-01 04:43:00+00:00  22.317329  113.926414         0             1               0    261    1618

[343 rows x 8 columns]
# --8<-- [end:df0]
"""
