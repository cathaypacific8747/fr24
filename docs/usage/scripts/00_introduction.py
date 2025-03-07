# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script]
import asyncio
from fr24 import FR24

async def main() -> None: # (1)!
    async with FR24() as fr24:
        result = await fr24.live_feed.fetch() # (2)!
        print(result)
        print(result.to_proto())
        print(result.to_dict())
        print(result.to_polars())

if __name__ == "__main__":
    asyncio.run(main())  # (3)!
# --8<-- [end:script]
# %%
"""
# --8<-- [start:result]
LiveFeedResult(
    request=LiveFeedParams(
        bounding_box=BoundingBox(south=42, north=52, west=-8, east=10),
        stats=False,
        limit=1500,
        maxage=14400,
        fields={'type', 'route', 'flight', 'reg'}
    ),
    response=<Response [200 OK]>,
    timestamp=1741365506
)
# --8<-- [end:result]
# --8<-- [start:result-proto]
flights_list {
  flightid: 962751826
  lat: 42.1471863
  lon: -6.79849291
  track: 15
  alt: 45000
  speed: 478
  icon: LJ60
  timestamp: 1741365503
  extra_info {
    type: "E55P"
  }
  position_buffer {
    recent_positions_list {
      delta_lat: 190
      delta_lon: 70
      delta_ms: 1074
    }
    recent_positions_list {
      delta_lat: 405
      delta_lon: 146
      delta_ms: 2092
    }
    recent_positions_list {
      delta_lat: 885
...
  timestamp_ms: 1741365503412
}
server_time_ms: 1741365506194
# --8<-- [end:result-proto]
# --8<-- [start:result-dict]
{
    'flightsList': [
        {
            'flightid': 962751826,
            'lat': 42.147186,
            'lon': -6.798493,
            'track': 15,
            'alt': 45000,
            'speed': 478,
            'icon': 'LJ60',
            'timestamp': 1741365503,
            'extraInfo': {'type': 'E55P'},
            'positionBuffer': {
                'recentPositionsList': [
                    {'deltaLat': 190, 'deltaLon': 70, 'deltaMs': 1074},
                    {'deltaLat': 405, 'deltaLon': 146, 'deltaMs': 2092},
                    {'deltaLat': 885, 'deltaLon': 323, 'deltaMs': 4250},
                    {'deltaLat': 1100, 'deltaLon': 404, 'deltaMs': 5540},
                    {'deltaLat': 1420, 'deltaLon': 516, 'deltaMs': 6570},
                    {'deltaLat': 1869, 'deltaLon': 685, 'deltaMs': 8740},
                    {'deltaLat': 2079, 'deltaLon': 759, 'deltaMs': 9820}
                ]
            },
            'timestampMs': '1741365503377'
        },
...
    ],
    'serverTimeMs': '1741365506194'
}
# --8<-- [end:result-dict]
# --8<-- [start:result-polars]
shape: (1_383, 18)
┌────────────┬───────────┬───────────┬───────────┬───┬─────┬───────────────┬────────┬──────────────┐
│ timestamp  ┆ flightid  ┆ latitude  ┆ longitude ┆ … ┆ eta ┆ vertical_spee ┆ squawk ┆ position_buf │
│ ---        ┆ ---       ┆ ---       ┆ ---       ┆   ┆ --- ┆ d             ┆ ---    ┆ fer          │
│ u32        ┆ u32       ┆ f32       ┆ f32       ┆   ┆ u32 ┆ ---           ┆ u16    ┆ ---          │
│            ┆           ┆           ┆           ┆   ┆     ┆ i16           ┆        ┆ list[struct[ │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 3]]          │
╞════════════╪═══════════╪═══════════╪═══════════╪═══╪═════╪═══════════════╪════════╪══════════════╡
│ 1741365503 ┆ 962751826 ┆ 42.147186 ┆ -6.798493 ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{190,70,107 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 4}, {405,146 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ ,2092}…      │
│ 1741365502 ┆ 962816491 ┆ 42.135269 ┆ -6.858715 ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{-96,193,10 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 61}, {-186,3 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 78,210…      │
│ 1741365502 ┆ 962797796 ┆ 42.508209 ┆ -7.829132 ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{-241,-86,1 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 027}, {-422, │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ -150,2…      │
│ 1741365502 ┆ 962807077 ┆ 42.617691 ┆ -7.186656 ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{-153,-178, │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 1140},       │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ {-294,-340,… │
│ 1741365503 ┆ 962798031 ┆ 43.173149 ┆ -6.419874 ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{-326,-189, │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 2087},       │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ {-481,-283,… │
│ …          ┆ …         ┆ …         ┆ …         ┆ … ┆ …   ┆ …             ┆ …      ┆ …            │
│ 1741365502 ┆ 962810249 ┆ 51.088894 ┆ 9.924316  ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{-215,-123, │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 1005},       │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ {-366,-205,… │
│ 1741365500 ┆ 962779754 ┆ 51.545338 ┆ 9.681549  ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{-45,-475,4 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 751}, {-60,- │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 579,64…      │
│ 1741365502 ┆ 962810708 ┆ 51.785828 ┆ 9.941025  ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{162,83,103 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 0}, {395,205 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ ,2080}…      │
│ 1741365502 ┆ 962800000 ┆ 51.911652 ┆ 9.614821  ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ []           │
│ 1741365503 ┆ 962808335 ┆ 51.924786 ┆ 9.956282  ┆ … ┆ 0   ┆ 0             ┆ 0      ┆ [{220,60,105 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ 8}, {377,102 │
│            ┆           ┆           ┆           ┆   ┆     ┆               ┆        ┆ ,2359}…      │
└────────────┴───────────┴───────────┴───────────┴───┴─────┴───────────────┴────────┴──────────────┘
# --8<-- [end:result-polars]
"""
#%%
# --8<-- [start:script-1]
from fr24 import FR24

async def my_feed() -> None:
    async with FR24() as fr24:
        ...
# --8<-- [end:script-1]
#%%
# --8<-- [start:login]
from fr24 import FR24

async def main() -> None:
    async with FR24() as fr24:
        # anonymous now
        await fr24.login() # reads from environment or configuration file, or,
        await fr24.login(creds={"username": "...", "password": "..."}) # or,
        await fr24.login(creds={"subscriptionKey": "...", "token": "..."})
# --8<-- [end:login]
#%%
# --8<-- [start:client-sharing]
import httpx

from fr24 import FR24

client = httpx.AsyncClient(http1=False, http2=True, transport=httpx.AsyncHTTPTransport(retries=5))

async def main() -> None:
    async with FR24(client) as fr24:
        ...
# --8<-- [end:client-sharing]
# %%
# --8<-- [start:script-2]
from fr24 import FR24

async def my_feed() -> None:
    async with FR24() as fr24:
        result = await fr24.live_feed.fetch()
        print(result.response.content)
# --8<-- [end:script-2]

# %%
"""
# --8<-- [start:result-response-content]
b'...truncated
\x84\x02(\xa2\x160m8\x03@\x00H\xfc\xc1\xac\xbe\x06P\x00Z\x05DEGLC`\x00j\x1c\n\x00\x12\x06D-EGLC\x1a\n\n\x03KSF\x12
\x03EIB"\x04C172r6\n\x19\x08\xd3\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\xa5\xfc\xff\xff\xff\xff\xff\xff\xff\x01\x18
\x8f%\n\x19\x08\xc4\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\xbd\xfb\xff\xff\xff\xff\xff\xff\xff\x01\x18\xb42x\xf5
\xb0\xe3\x8b\xd72\n\x96\x01\x08\xd4\xa6\x8d\xcb\x03\x15\xb0$OB\x1dp\x0e\x1fA 
\x12(\xbar0\xf3\x028\x05@\x00H\xfe\xc1\xac\xbe\x06P\x00Z\x06ECA4RT`\x00j\x1c\n\x00\x12\x06D-CFRT\x1a\n\n\x03FMM\x12
\x03HAJ"\x04C25CrA\n\x08\x08\xa2\x01\x10S\x18\x86\x08\n\t\x08\x8b\x03\x10\xcd\x01\x18\xa0\x10\n\t\x08\xd1\x05\x10
\xf5\x02\x18\x8c!\n\t\x08\xf9\x06\x10\xd1\x03\x18\xac*\n\t\x08\xb7\n\x10\xbc\x05\x18\x8c=\n\t\x08\xed\x0b\x10\xa1\x06
\x18\x9fEx\xf0\xc4\xe3\x8b\xd72\nN\x08\x80\xd3\x8c\xcb\x03\x15\x88\xa5OB\x1dO\xd6\x19A 
\xf2\x01(\x96\x1a0\n8\x03@\x00H\xfe\xc1\xac\xbe\x06P\x00Z\x05DEGZZ`\x01j\x16\n\x00\x12\x06D-EGZZ\x1a\x04\n\x00\x12
\x00"\x04DA40r\x00x\xc4\xc1\xe3\x8b\xd72\n\x9c\x01\x08\x8f\x94\x8d\xcb\x03\x15\xfb\xb2OB\x1d\xeeL\x1fA 
\n(\xa1Y0\xd6\x028\x07@\x00H\xff\xc1\xac\xbe\x06P\x00Z\x07AFR87MJ`\x00j"\n\x06AF1838\x12\x06F-HBXE\x1a\n\n\x03CDG
\x12\x03HAJ"\x04E170r@\n\x08\x08\xdc\x01\x10<\x18\xa2\x08\n\x08\x08\xf9\x02\x10f\x18\xb7\x12\n\t\x08\xed\x05\x10\xd3
\x01\x18\x82&\n\t\x08\x9e\x07\x10\x8a\x02\x18\xbd.\n\t\x08\xb9\x08\x10\xb8\x02\x18\xa76\n\t\x08\xb5\x0b\x10\xa3\x03
\x18\xa1Gx\xb4\xcb\xe3\x8b\xd72 \x92\xe1\xe3\x8b\xd72\x80\x00\x00\x00\x0fgrpc-status:0\r\n'
# --8<-- [end:result-response-content]
"""
#%%
# --8<-- [start:script-3]
import asyncio
from fr24 import FR24

async def main() -> None:
    async with FR24() as fr24:
        result = await fr24.live_feed.fetch()
        print(result.to_proto())
        print(result.to_dict())
        print(result.to_polars())
# --8<-- [end:script-3]
#%%
# --8<-- [start:script-4]
import asyncio
import json
from fr24 import FR24

async def main() -> None:
    async with FR24() as fr24:
        result = await fr24.live_feed.fetch()
        with open("path/to/some/file.json", "w") as f:
            json.dump(result.to_dict(), f, indent=4)
# --8<-- [end:script-4]
#%%
# --8<-- [start:script-5]
import asyncio
from io import BytesIO
from fr24 import FR24

async def main() -> None:
    async with FR24() as fr24:
        result = await fr24.live_feed.fetch()
        result.write_table("path/to/some/file.parquet") # (1)!
        result.write_table("path/to/some/file.csv", format="csv") # (2)!

        buffer = BytesIO()
        result.write_table(buffer, format="parquet")
        buffer.seek(0)
# --8<-- [end:script-5]
#%%
# --8<-- [start:script-6]
import asyncio
from fr24 import FR24, FR24Cache

cache = FR24Cache("path/to/some/directory/")
# alternatively, use the default cache directory:
cache = FR24Cache.default() # (1)!

async def main() -> None:
    async with FR24() as fr24:
        result = await fr24.live_feed.fetch()
        result.write_table(cache)
# --8<-- [end:script-6]
#%%
# --8<-- [start:script-7]
from fr24 import FR24Cache

cache = FR24Cache.default()

for fp in cache.live_feed.glob("*"):
    print(fp)
    lf = cache.live_feed.scan_table(fp)
    print(lf.collect())

# alternatively, scan one file:
lf = cache.live_feed.scan_table("1733036597")
# --8<-- [end:script-7]
#%%
"""
# --8<-- [start:output-7]
/home/user/.cache/fr24/feed/1733036597.parquet
# --8<-- [end:output-7]
"""
# %%
