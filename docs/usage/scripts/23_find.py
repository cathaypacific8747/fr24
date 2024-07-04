# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
from fr24.types.find import FindResult
from fr24.find import find

import pandas as pd
import httpx

async def my_find() -> FindResult:
    async with httpx.AsyncClient() as client:
        results = await find(client, "paris")
        assert results is not None
        return results


results = await my_find()
pd.DataFrame(pd.json_normalize(results["results"]))
# --8<-- [end:script0]
# %%
"""
# --8<-- [start:df0]
    id                                            label     type   match  detail.lat  detail.lon  detail.size
0  CDG     Paris Charles de Gaulle Airport (CDG / LFPG)  airport  begins   49.012516    2.555752       199939
1  ORY                  Paris Orly Airport (ORY / LFPO)  airport  begins   48.723331    2.379444        87577
2  LBG            Paris Le Bourget Airport (LBG / LFPB)  airport  begins   48.958801    2.433600        27873
3  BVA        Paris Beauvais-Tille Airport (BVA / LFOB)  airport  begins   49.454189    2.113550        16566
4  PRX                     Paris Cox Field (PRX / KPRX)  airport  begins   33.636665  -95.450279         1402
5  XCR         Paris Vatry Chalons Airport (XCR / LFOK)  airport  begins   48.759998    4.200000         1008
6  VIY  Paris Villacoublay Velizy Air Base (VIY / LFPV)  airport  begins   48.774399    2.201540          993
7  PHT          Paris Henry County Airport (PHT / KPHT)  airport  begins   36.336384  -88.384270          390
# --8<-- [end:df0]
"""
