# ruff: noqa
# fmt: off
#%%
# --8<-- [start:script0]
import rich
from fr24.core import FR24

async def my_playback() -> None:
    async with FR24() as fr24:
        response = await fr24.playback.fetch(0x2FB3041)  # (1)!
        data = response.to_arrow()
        print(data.df)
        rich.print(data.metadata)
        data.save()

await my_playback()
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:df0]
      timestamp   latitude  longitude  altitude  ground_speed  vertical_speed  track  squawk   ems
0    1232049993  40.770302 -73.862801         0             0             NaN     59       0  None
1    1232049997  40.770302 -73.862503         0             0             NaN     65       0  None
2    1232050001  40.770302 -73.862198         0             0             NaN     71       0  None
3    1232050005  40.770302 -73.862198         0             0             NaN     76       0  None
4    1232050009  40.770302 -73.862198         0             0             NaN     82       0  None
..          ...        ...        ...       ...           ...             ...    ...     ...   ...
358  1232051425  40.781399 -73.998199       326           137             NaN    223       0  None
359  1232051429  40.779202 -73.999603       274           131             NaN    226       0  None
360  1232051433  40.777199 -74.001297       187           134             NaN    222       0  None
361  1232051437  40.775002 -74.002899       106           130             NaN    223       0  None
362  1232051441  40.773102 -74.004303        42           128             NaN    223       0  None

[363 rows x 9 columns]
# --8<-- [end:df0]
"""
#%%
# --8<-- [start:metadata0]
{
    'flight_id': 50016321,
    'callsign': 'AWE1549',
    'flight_number': 'UA1549',
    'status_type': 'departure',
    'status_text': None,
    'status_diverted': None,
    'status_time': None,
    'model_code': 'A320',
    'icao24': 10493137,
    'registration': 'N106US',
    'owner': None,
    'airline': None,
    'origin': 'KLGA',
    'destination': 'KCLT',
    'median_delay': None,
    'median_time': None
}
# --8<-- [end:metadata0]

#%%
# --8<-- [start:script1]
import rich
from fr24.core import FR24

async def my_playback() -> None:
    async with FR24() as fr24:
        response = await fr24.playback.fetch(0x2FB3041)
        data = response.to_arrow()
        data.save()  # (1)!
        # some time later...
        data_local = fr24.playback.load(0x2FB3041)  # (2)!
        print(data_local.df)
        rich.print(data_local.metadata)

await my_playback()
# --8<-- [end:script1]

# %%
