# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx

from fr24.types.airport_list import AirportList
from fr24.json import airport_list, AirportListParams

import pandas as pd

async def my_arrivals() -> AirportList:
    async with httpx.AsyncClient() as client:
        response = await airport_list(
            client,
            AirportListParams(airport="tls", mode="arrivals"),
        )
        response.raise_for_status()
        list_ = response.json()
        return list_ # type: ignore


airports = await my_arrivals()
pd.DataFrame(
    pd.json_normalize(
        airports["result"]["response"]["airport"]["pluginData"]["schedule"][
            "arrivals"
        ]["data"]
    )
)
# --8<-- [end:script0]
# %%
"""
# --8<-- [start:df0]
    flight.identification.id   flight.identification.row   flight.identification.number.default   flight.identification.number.alternative   flight.identification.callsign   flight.identification.codeshare   flight.status.live   flight.status.text   flight.status.icon   flight.status.estimated   ...   flight.time.scheduled.departure   flight.time.scheduled.arrival   flight.time.real.departure   flight.time.real.arrival   flight.time.estimated.departure   flight.time.estimated.arrival   flight.time.other.eta   flight.time.other.duration   flight.aircraft.images   flight.owner  
0                       None                  5488300922                                 FR8125                                    MAY8125                          RYR8125                              None                False            Scheduled                 None                      None   ...                        1711986600                      1711991100                         None                       None                      1.711987e+09                            None                    None                         None                      NaN            NaN  
1                       None                  5488216841                                 AF6124                                       None                             None                              None                False            Scheduled                 None                      None   ...                        1711987200                      1711991700                         None                       None                               NaN                            None                    None                         None                      NaN            NaN  
2                       None                  5488418617                                 U24849                                     EC4849                          EJU51KM                              None                False            Scheduled                 None                      None   ...                        1711987500                      1711992000                         None                       None                      1.711988e+09                            None                    None                         None                      NaN            NaN  
3                       None                  5488418658                                 U24988                                     EC4988                          EJU82LE                              None                False            Scheduled                 None                      None   ...                        1711986900                      1711992300                         None                       None                      1.711987e+09                            None                    None                         None                      NaN            NaN  
4                       None                  5488216846                                 AF6126                                       None                             None                              None                False            Scheduled                 None                      None   ...                        1711989000                      1711993500                         None                       None                               NaN                            None                    None                         None                      NaN            NaN  
5                       None                  5488417705                                 U21311                                     DS1311                          EZS15PY                              None                False            Scheduled                 None                      None   ...                        1711990500                      1711995000                         None                       None                      1.711990e+09                            None                    None                         None                      NaN            NaN  
6                       None                  5488297888                                 FR1995                                    MAY1995                          RYR1995                              None                False            Scheduled                 None                      None   ...                        1711989600                      1711996500                         None                       None                      1.711990e+09                            None                    None                         None                      NaN            NaN  
7                       None                  5488418631                                 U24851                                     EC4851                          EJU69EW                              None                False            Scheduled                 None                      None   ...                        1711992000                      1711996500                         None                       None                      1.711992e+09                            None                    None                         None                      NaN            NaN  
8                       None                  5488298693                                 FR3358                                       None                             None                              None                False            Scheduled                 None                      None   ...                        1711986900                      1711996800                         None                       None                      1.711987e+09                            None                    None                         None                      NaN            NaN  
9                       None                  5488418589                                 U24729                                     EC4729                          EJU89CR                              None                False            Scheduled                 None                      None   ...                        1711993200                      1711997400                         None                       None                      1.711993e+09                            None                    None                         None                      NaN            NaN  

[10 rows x 75 columns]
# --8<-- [end:df0]
"""
