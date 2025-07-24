# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script]
from fr24 import FR24, FR24Cache

async def get_farthest_flight_id(fr24: FR24) -> int:
    nearest_result = await fr24.nearest_flights.fetch(
        lat=22.31257, lon=113.92708, radius=10000, limit=1500
    )
    return nearest_result.to_proto().flights_list[-1].flight.flightid

async def my_flight_details() -> None:
    async with FR24() as fr24:
        flight_id = await get_farthest_flight_id(fr24)
        result = await fr24.flight_details.fetch(flight_id=flight_id)
        print(result)
        print(result.to_dict())
        print(result.to_polars())
        result.write_table(FR24Cache.default())

await my_flight_details()
# --8<-- [end:script]

# %%
"""
# --8<-- [start:result]
FlightDetailsResult(
    request=FlightDetailsParams(flight_id=981435745, restriction_mode=0, verbose=True),
    response=<Response [200 OK]>,
    timestamp=1748198596
)
# --8<-- [end:result]
# --8<-- [start:dict]
{
    'aircraft_info': {
        'icao_address': 7901836,
        'reg': 'B-LPR',
        'type': 'A321',
        'icon': 'A320',
        'full_description': 'Airbus A321-231',
        'images_list': [
            {
                'url': 'https://www.jetphotos.com/photo/11710285',
                'copyright': 'Hayashi_008',
                'thumbnail': 'https://cdn.jetphotos.com/200/5/1052205_1745736486_tb.jpg',
                'medium': 'https://cdn.jetphotos.com/400/5/1052205_1745736486.jpg',
                'large': 'https://cdn.jetphotos.com/640/5/1052205_1745736486.jpg'
            },
            {
                'url': 'https://www.jetphotos.com/photo/11710266',
                'copyright': 'Jhang yao yun',
                'thumbnail': 'https://cdn.jetphotos.com/200/6/430972_1745733519_tb.jpg',
                'medium': 'https://cdn.jetphotos.com/400/6/430972_1745733519.jpg',
                'large': 'https://cdn.jetphotos.com/640/6/430972_1745733519.jpg'
            },
            {
                'url': 'https://www.jetphotos.com/photo/11701103',
                'copyright': 'verduyn',
                'thumbnail': 'https://cdn.jetphotos.com/200/6/862976_1744865774_tb.jpg',
                'medium': 'https://cdn.jetphotos.com/400/6/862976_1744865774.jpg',
                'large': 'https://cdn.jetphotos.com/640/6/862976_1744865774.jpg'
            }
        ],
        'msn_available': True,
        'age_available': True,
        'registered_owners': 'Hong Kong Airlines',
        'is_country_of_reg_available': True
    },
    'schedule_info': {
        'flight_number': 'HX606',
        'operated_by_id': 641,
        'painted_as_id': 641,
        'origin_id': 1366,
        'destination_id': 2505,
        'scheduled_departure': 1748198100,
        'scheduled_arrival': 1748215200,
        'arr_terminal': '1'
    },
    'flight_progress': {
        'traversed_distance': 2389,
        'remaining_distance': 2964062,
        'great_circle_distance': 2963825,
        'mean_flight_time': 13490,
        'flight_stage': 'ON_GROUND'
    },
    'flight_info': {
        'flightid': 981435745,
        'lat': 22.325708,
        'lon': 113.90078,
        'track': 250,
        'speed': 14,
        'timestamp_ms': '1748198593883',
        'on_ground': True,
        'callsign': 'CRK606',
        'ems_availability': {},
        'squawk_availability': True,
        'airspace_availability': True,
        'server_time_ms': '1748198596450'
    },
    'flight_plan': {},
    'flight_trail_list': [
        {'snapshot_id': '1748197476', 'lat': 22.30672, 'lon': 113.9181, 'heading': 180},
        ...
        {'snapshot_id': '1748198570', 'lat': 22.32614, 'lon': 113.90211, 'spd': 9, 'heading': 247},
        {'snapshot_id': '1748198575', 'lat': 22.32605, 'lon': 113.901855, 'spd': 10, 'heading': 250}
    ]
}
# --8<-- [end:dict]
# --8<-- [start:polars]
shape: (1, 31)
┌─────────────┬───────┬──────────┬─────────────┬───┬──────────┬────────┬─────────────┬─────────────┐
│ icao_addres ┆ reg   ┆ typecode ┆ flight_numb ┆ … ┆ callsign ┆ squawk ┆ ems         ┆ flight_trai │
│ s           ┆ ---   ┆ ---      ┆ er          ┆   ┆ ---      ┆ ---    ┆ ---         ┆ l_list      │
│ ---         ┆ str   ┆ str      ┆ ---         ┆   ┆ str      ┆ u16    ┆ struct[13]  ┆ ---         │
│ u32         ┆       ┆          ┆ str         ┆   ┆          ┆        ┆             ┆ list[struct │
│             ┆       ┆          ┆             ┆   ┆          ┆        ┆             ┆ [7]]        │
╞═════════════╪═══════╪══════════╪═════════════╪═══╪══════════╪════════╪═════════════╪═════════════╡
│ 7901836     ┆ B-LPR ┆ A321     ┆ HX606       ┆ … ┆ CRK606   ┆ 0      ┆ {0,0,0,0,0, ┆ [{174819747 │
│             ┆       ┆          ┆             ┆   ┆          ┆        ┆ 0,0,0,0,0,0 ┆ 6,22.306721 │
│             ┆       ┆          ┆             ┆   ┆          ┆        ┆ ,0,0}       ┆ ,113.918…   │
└─────────────┴───────┴──────────┴─────────────┴───┴──────────┴────────┴─────────────┴─────────────┘
# --8<-- [end:polars]
"""
