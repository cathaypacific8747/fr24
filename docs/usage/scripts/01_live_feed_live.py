# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script]
from fr24 import FR24

async def my_feed() -> None:
    async with FR24() as fr24:
        response = await fr24.live_feed.fetch()
        datac = response.to_arrow()
        datac.save()

await my_feed()
# --8<-- [end:script]
# %%
# --8<-- [start:script2]
from fr24 import FR24

async def my_feed() -> None:
    async with FR24() as fr24:
        datac = fr24.live_feed.load(1733036597)

await my_feed()
# --8<-- [end:script2]
# %%
"""
# --8<-- [start:response]
LiveFeedAPIResp(
    ctx={
        "timestamp": 1733036597,
        "source": "live",
        "duration": None,
        "hfreq": None,
        "limit": 1500,
        "fields": ["flight", "reg", "route", "type"],
        "base_dir": PosixPath("/home/user/.cache/fr24"),
    },
    data=[
        {
            "timestamp": 1733036585,
            "flightid": 942542957,
            "latitude": -12.017459869384766,
            "longitude": -175.8354034423828,
            "track": 48,
            "altitude": 32000,
            "ground_speed": 500,
            "vertical_speed": 0,
            "on_ground": False,
            "callsign": "AAL72",
            "source": 0,
            "registration": "N729AN",
            "origin": "SYD",
            "destination": "LAX",
            "typecode": "B77W",
            "eta": 0,
            "squawk": 0,
            "position_buffer": [
                {"delta_lat": 432, "delta_lon": 494, "delta_ms": 2360}
            ],
        },
        {
            "timestamp": 1733036595,
            "flightid": 942552952,
            "latitude": -29.51480484008789,
            "longitude": -174.44357299804688,
            "track": 43,
            "altitude": 29004,
            "ground_speed": 525,
            "vertical_speed": 0,
            "on_ground": False,
            "callsign": "ANZ4",
            "source": 5,
            "registration": "ZK-OKQ",
            "origin": "AKL",
            "destination": "LAX",
            "typecode": "B77W",
            "eta": 0,
            "squawk": 0,
            "position_buffer": [
                {"delta_lat": 831, "delta_lon": 892, "delta_ms": 4687},
                {"delta_lat": 1609, "delta_lon": 1727, "delta_ms": 9068},
            ],
        },
        # ...
    ]
)
# --8<-- [end:response]
"""
#%%
"""
# --8<-- [start:df]
        timestamp   flightid   latitude   longitude  track  altitude  ground_speed  on_ground callsign  source registration origin destination typecode  eta  vertical_speed  squawk                                   position_buffer  
0      1733036585  942542957 -12.017460 -175.835403     48     32000           500      False    AAL72       0       N729AN    SYD         LAX     B77W    0               0       0 [{'delta_lat': 432, 'delta_lon': 494, 'delta_m...  
1      1733036595  942552952 -29.514805 -174.443573     43     29004           525      False     ANZ4       5       ZK-OKQ    AKL         LAX     B77W    0               0       0 [{'delta_lat': 831, 'delta_lon': 892, 'delta_m...  
2      1733036595  942533540  -5.759705 -168.846771     47     37000           494      False   UAL100       5       N27965    SYD         IAH     B789    0               0       0 [{'delta_lat': 727, 'delta_lon': 793, 'delta_m...  
3      1733036595  942536182  -4.503380 -179.264038     53     37000           514      False    QFA93       3       VH-ZNE    MEL         LAX     B789    0               0       0 [{'delta_lat': 670, 'delta_lon': 894, 'delta_m...  
4      1733036592  942537131  -3.225645 -177.020752     59     32000           512      False   UAL830       5       N2333U    SYD         SFO     B77W    0               0       0 [{'delta_lat': 463, 'delta_lon': 775, 'delta_m...  
...           ...        ...        ...         ...    ...       ...           ...        ...      ...     ...          ...    ...         ...      ...  ...             ...     ...                                               ...  
11397  1733036592  942548650  55.756233  174.116119    237     32000           520      False  CPA3283       4        B-LJM    ANC         HKG     B748    0               0       0 [{'delta_lat': -586, 'delta_lon': -1608, 'delt...  
11398  1733036592  942519223  57.377785  176.103302    234     38000           468      False  KAL9284       3       HL8252    YYZ         ICN     B77L    0               0       0 [{'delta_lat': -484, 'delta_lon': -1239, 'delt...  
11399  1733036592  942521821  55.513550  176.156662     48     31000           493      False   KAL093       5       HL8041    ICN         IAD     B77W    0               0       0 [{'delta_lat': 682, 'delta_lon': 1342, 'delta_...  
11400  1733036595  942532958  64.681732  179.871552    274     36000           469      False  CAO1058       0       B-2098    LAX         PEK     B77L    0               0       0 [{'delta_lat': 60, 'delta_lon': -2018, 'delta_...  
11401  1733036592  942550038  57.237507  178.640396    241     37000           494      False   NCA167       4       JA18KZ    ANC         NRT     B748    0               0       0 [{'delta_lat': -495, 'delta_lon': -1657, 'delt...  

[11402 rows x 18 columns]
# --8<-- [end:df]
"""
