# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
from fr24.types.find import Find
from fr24.json import find

import polars as pl
import httpx

async def my_find() -> Find:
    async with httpx.AsyncClient() as client:
        response = await find(client, "paris")
        response.raise_for_status()
        results = response.json()
        return results  # type: ignore


results = await my_find()
df = pl.json_normalize(results["results"])
print(df)
# --8<-- [end:script0]
# %%
"""
# --8<-- [start:df0]
shape: (9, 7)
┌─────┬───────────────────────────────┬─────────┬──────────┬────────────┬────────────┬─────────────┐
│ id  ┆ label                         ┆ type    ┆ match    ┆ detail.lat ┆ detail.lon ┆ detail.size │
│ --- ┆ ---                           ┆ ---     ┆ ---      ┆ ---        ┆ ---        ┆ ---         │
│ str ┆ str                           ┆ str     ┆ str      ┆ f64        ┆ f64        ┆ i64         │
╞═════╪═══════════════════════════════╪═════════╪══════════╪════════════╪════════════╪═════════════╡
│ CDG ┆ Paris Charles de Gaulle       ┆ airport ┆ begins   ┆ 49.012516  ┆ 2.555752   ┆ 201280      │
│     ┆ Airpor…                       ┆         ┆          ┆            ┆            ┆             │
│ ORY ┆ Paris Orly Airport (ORY /     ┆ airport ┆ begins   ┆ 48.723331  ┆ 2.379444   ┆ 84510       │
│     ┆ LFPO…                         ┆         ┆          ┆            ┆            ┆             │
│ LBG ┆ Paris Le Bourget Airport (LBG ┆ airport ┆ begins   ┆ 48.958801  ┆ 2.4336     ┆ 24465       │
│     ┆ …                             ┆         ┆          ┆            ┆            ┆             │
│ BVA ┆ Paris Beauvais-Tille Airport  ┆ airport ┆ begins   ┆ 49.453465  ┆ 2.115138   ┆ 15939       │
│     ┆ (…                            ┆         ┆          ┆            ┆            ┆             │
│ VIY ┆ Paris Villacoublay Velizy Air ┆ airport ┆ begins   ┆ 48.774399  ┆ 2.20154    ┆ 1038        │
│     ┆ …                             ┆         ┆          ┆            ┆            ┆             │
│ PRX ┆ Paris Cox Field (PRX / KPRX)  ┆ airport ┆ begins   ┆ 33.636665  ┆ -95.450279 ┆ 953         │
│ XCR ┆ Paris Vatry Chalons Airport   ┆ airport ┆ begins   ┆ 48.759998  ┆ 4.2        ┆ 710         │
│     ┆ (X…                           ┆         ┆          ┆            ┆            ┆             │
│ PHT ┆ Paris Henry County Airport    ┆ airport ┆ begins   ┆ 36.336384  ┆ -88.38427  ┆ 199         │
│     ┆ (PH…                          ┆         ┆          ┆            ┆            ┆             │
│ OPL ┆ Opelousas St. Landry Parish   ┆ airport ┆ contains ┆ 30.555695  ┆ -92.098915 ┆ 194         │
│     ┆ Ai…                           ┆         ┆          ┆            ┆            ┆             │
└─────┴───────────────────────────────┴─────────┴──────────┴────────────┴────────────┴─────────────┘
# --8<-- [end:df0]
"""
