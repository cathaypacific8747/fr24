# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script]
from fr24 import FR24, FR24Cache
import polars as pl


async def get_last_flight(fr24: FR24, *, reg: str = "B-LRA") -> tuple[int, int]:
    flight_list_result = await fr24.flight_list.fetch(reg=reg)
    df = flight_list_result.to_polars()

    landed = df.filter(pl.col("status").str.starts_with("Landed"))
    assert landed.height > 0, "no landed flights found"

    flight_id = landed[0, "flight_id"]
    stod = int(landed[0, "ATOD"].timestamp())
    return flight_id, stod


async def my_playback_flight() -> None:
    async with FR24() as fr24:
        flight_id, timestamp = await get_last_flight(fr24)
        result = await fr24.playback_flight.fetch(
            flight_id=flight_id, timestamp=timestamp
        )
        print(result)
        print(result.to_dict())
        print(result.to_polars())
        result.write_table(FR24Cache.default())


await my_playback_flight()
# --8<-- [end:script]

# %%
"""
# --8<-- [start:result]
PlaybackFlightResult(
    request=PlaybackFlightParams(flight_id=981308334, timestamp=1748151914),
    response=<Response [200 OK]>
)
# --8<-- [end:result]
# --8<-- [start:dict]
{
    'aircraft_info': {
        'icao_address': 7867035,
        'reg': 'B-LRA',
        'type': 'A359',
        'icon': 'A330',
        'full_description': 'Airbus A350-941',
        'images_list': [
            {
                'url': 'https://www.jetphotos.com/photo/11633658',
                'copyright': 'lix1aolu',
                'thumbnail': 'https://cdn.jetphotos.com/200/6/850117_1739185739_tb.jpg',
                'medium': 'https://cdn.jetphotos.com/400/6/850117_1739185739.jpg',
                'large': 'https://cdn.jetphotos.com/640/6/850117_1739185739.jpg'
            },
            {
                'url': 'https://www.jetphotos.com/photo/11634217',
                'copyright': 'Waibibabu',
                'thumbnail': 'https://cdn.jetphotos.com/200/6/591483_1739217827_tb.jpg',
                'medium': 'https://cdn.jetphotos.com/400/6/591483_1739217827.jpg',
                'large': 'https://cdn.jetphotos.com/640/6/591483_1739217827.jpg'
            },
            {
                'url': 'https://www.jetphotos.com/photo/11620028',
                'copyright': 'ZBAA cao',
                'thumbnail': 'https://cdn.jetphotos.com/200/6/723478_1737987561_tb.jpg',
                'medium': 'https://cdn.jetphotos.com/400/6/723478_1737987561.jpg',
                'large': 'https://cdn.jetphotos.com/640/6/723478_1737987561.jpg'
            }
        ],
        'msn_available': True,
        'age_available': True,
        'registered_owners': 'Cathay Pacific',
        'is_country_of_reg_available': True
    },
    'schedule_info': {
        'flight_number': 'CX758',
        'operated_by_id': 57,
        'painted_as_id': 57,
        'origin_id': 3182,
        'destination_id': 1366,
        'scheduled_departure': 1748150700,
        'scheduled_arrival': 1748165700,
        'actual_departure': 1748151914,
        'actual_arrival': 1748164743,
        'arr_terminal': '1',
        'baggage_belt': '5'
    },
    'flight_info': {
        'flightid': 981308334,
        'lat': 1.3314638,
        'lon': 103.986115,
        'track': 22,
        'speed': 55,
        'timestamp_ms': '1748151902672',
        'on_ground': True,
        'callsign': 'CPA758',
        'ems_availability': {},
        'squawk_availability': True,
        'vspeed_availability': True,
        'airspace_availability': True,
        'server_time_ms': '1748202193168'
    },
    'flight_trail_list': [
        {'snapshot_id': '1748151113', 'lat': 1.341973, 'lon': 103.98659, 'heading': 202},
        {'snapshot_id': '1748151183', 'lat': 1.342232, 'lon': 103.98668, 'heading': 208},
        ...
        {'snapshot_id': '1748165435', 'lat': 22.314384, 'lon': 113.92283, 'spd': 3, 'heading': 42}
    ]
}
# --8<-- [end:dict]
# --8<-- [start:polars]
shape: (1, 24)
┌─────────────┬───────┬──────────┬─────────────┬───┬──────────┬────────┬─────────────┬─────────────┐
│ icao_addres ┆ reg   ┆ typecode ┆ flight_numb ┆ … ┆ callsign ┆ squawk ┆ ems         ┆ flight_trai │
│ s           ┆ ---   ┆ ---      ┆ er          ┆   ┆ ---      ┆ ---    ┆ ---         ┆ l_list      │
│ ---         ┆ str   ┆ str      ┆ ---         ┆   ┆ str      ┆ u16    ┆ struct[13]  ┆ ---         │
│ u32         ┆       ┆          ┆ str         ┆   ┆          ┆        ┆             ┆ list[struct │
│             ┆       ┆          ┆             ┆   ┆          ┆        ┆             ┆ [7]]        │
╞═════════════╪═══════╪══════════╪═════════════╪═══╪══════════╪════════╪═════════════╪═════════════╡
│ 7867035     ┆ B-LRA ┆ A359     ┆ CX758       ┆ … ┆ CPA758   ┆ 0      ┆ {0,0,0,0,0, ┆ [{174815111 │
│             ┆       ┆          ┆             ┆   ┆          ┆        ┆ 0,0,0,0,0,0 ┆ 3,1.341973, │
│             ┆       ┆          ┆             ┆   ┆          ┆        ┆ ,0,0}       ┆ 103.9865…   │
└─────────────┴───────┴──────────┴─────────────┴───┴──────────┴────────┴─────────────┴─────────────┘
# --8<-- [end:polars]
"""
