# ruff: noqa
# fmt: off
# %%
# --8<-- [start:script]
from fr24.core import FR24

async def my_feed() -> None:
    async with FR24() as fr24:
        response = await fr24.livefeed.fetch()
        datac = response.to_arrow()
        datac.save()

await my_feed()
# --8<-- [end:script]
# %%
# --8<-- [start:script2]
from fr24.core import FR24

async def my_feed() -> None:
    async with FR24() as fr24:
        datac = fr24.livefeed.load(1711911907)

await my_feed()
# --8<-- [end:script2]
# %%
# --8<-- [start:response]
LiveFeedAPIResp(
    ctx={
        "timestamp": 1711911907,
        "source": "live",
        "duration": None,
        "hfreq": None,
        "base_dir": PosixPath("/home/user/.cache/fr24"),
    },
    data=[
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
    ],
)
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
