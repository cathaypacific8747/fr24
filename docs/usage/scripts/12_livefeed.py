# ruff: noqa
# fmt: off
# %%
# --8<-- [start:script]
from fr24.core import FR24

async def my_feed() -> None:
    async with FR24() as fr24:
        lf = fr24.livefeed()
        response = await lf.api._fetch()
        print(response)
        lf.data._add_api_response(response)
        print(lf.data.df)
        lf.data._save_parquet()

await my_feed()
# --8<-- [end:script]
# %%
# --8<-- [start:response]
[
    {
        "timestamp": 1711911905,
        "flightid": 882151247,
        "latitude": -12.432657241821289,
        "longitude": -172.14825439453125,
        "heading": 203,
        "altitude": 34000,
        "ground_speed": 515,
        "vertical_speed": 0,
        "on_ground": False,
        "callsign": "QFA7552",
        "source": 0,
        "registration": "N409MC",
        "origin": "HNL",
        "destination": "AKL",
        "typecode": "B744",
        "eta": 0,
    }
    # ... 15109 more items
]
# --8<-- [end:response]
#%%
"""
# --8<-- [start:df]
        timestamp   flightid   latitude   longitude  heading  altitude  ground_speed  on_ground callsign  source registration origin  destination typecode  eta  vertical_speed
0      1711911905  882151247 -12.432657 -172.148254      203     34000           515      False  QFA7552       0       N409MC    HNL          AKL     B744    0               0
1      1711911902  882203620 -16.504490 -178.940308      249     36000           460      False    VOZ76       0       VH-YIL    APW          BNE     B738    0               0
2      1711911904  882212062 -13.240505 -176.195602      292         0             0       True  RLY0100       0       F-OCQZ    WLS                  DHC6    0               0
3      1711911897  882145424  10.347591 -167.007263       56     37000           516      False    QFA15       5       VH-EBQ    BNE          LAX     A332    0               0
4      1711911905  882199081  18.591330 -165.391083      247     32000           416      False   UAL132       3       N77296    HNL          MAJ     B738    0               0
...           ...        ...        ...         ...      ...       ...           ...        ...      ...     ...          ...    ...          ...      ...  ...             ...
15095  1711911897  882140495  53.746582  174.467392      258     38000           435      False  GTI8650       5       N710GT    LAX          HKG     B77L    0               0
15096  1711911887  882155955  54.291172  175.606842       57     31000           515      False    UPS81       5       N628UP    PVG          ANC     B748    0               0
15097  1711911673  882165589  57.548691  179.460800      246     36000           438      False   KAL258       4       HL8285    ANC          ICN     B77L    0               0
15098  1711911901  882187089  56.527115  176.298798      242     38000           442      False   CKS936       4       N701CK    ANC          HFE     B744    0               0
15099  1711911905  882137160  59.153641  179.730972      229     38000           471      False  KAL8286       5       HL8043    YYZ          ICN     B77L    0               0

[15100 rows x 16 columns]
# --8<-- [end:df]
"""
# %%
# --8<-- [start:script2]
from fr24.core import FR24
import time

async def my_feed() -> None:
    async with FR24() as fr24:
        lf = fr24.livefeed(int(time.time() - 86400 * 3))  # (1)!
        lf.data._add_api_response(await lf.api._fetch())
        print(lf.data.df)

await my_feed()
# --8<-- [end:script2]

# %%
"""
# --8<-- [start:df2]
        timestamp   flightid   latitude   longitude  heading  altitude ground_speed  on_ground callsign  source registration origin destination typecode  eta  vertical_speed
0      1711697713  881642343 -13.628512 -169.556046       44     37000          499      False    DAL42       0       N519DN    SYD         LAX     A359    0               0
1      1711697709  881686001 -14.096649 -172.093018      182      8850          298      False   ANZ999       0       ZK-NNE    APW         AKL     A21N    0               0
2      1711697713  881673319 -46.344315 -173.242355      122     31975          568      False   LAN800       4       CC-BGC    AKL         SCL     B789    0               0
3      1711697713  881679659 -34.398090 -178.388153       64     37975          530      False   ANZ902       4       ZK-NZE    AKL         PPT     B789    0               0
4      1711697717  881655685 -12.116470 -169.877808      199     36000          469      False   HAL465       5       N395HA    HNL         PPG     A332    0               0
...           ...        ...        ...         ...      ...       ...          ...        ...      ...     ...          ...    ...         ...      ...  ...             ...
11422  1711697721  881662489  56.048801  174.987000      240     36000          468      False  CPA3187       3        B-LJG    ANC         HKG     B748    0               0
11423  1711697713  881602916  56.870163  175.223923      226     35000          476      False   ANA111       3       JA796A    ORD         HND     B77W    0               0
11424  1711697713  881669755  56.652039  176.742554      240     34000          459      False  FDX5236       3       N573FE    ANC         ICN     MD11    0               0
11425  1711697721  881652749  57.509033  179.559845      242     38000          467      False  GTI8065       3       N452PA    PDX         ICN     B744    0               0
11426  1711697717  881648986  54.571342  175.497025       55     31000          501      False   EVA662       5      B-16781    TPE         ANC     B77L    0               0

[11427 rows x 16 columns]
# --8<-- [end:df2]
"""
