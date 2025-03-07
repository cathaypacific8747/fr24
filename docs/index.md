# fr24

[![image](https://img.shields.io/pypi/v/fr24.svg)](https://pypi.python.org/pypi/fr24)
[![image](https://img.shields.io/pypi/l/fr24.svg)](https://pypi.python.org/pypi/fr24)
[![image](https://img.shields.io/pypi/pyversions/fr24.svg)](https://pypi.python.org/pypi/fr24)
[![image](https://img.shields.io/pypi/status/fr24)](https://pypi.python.org/pypi/fr24)

`fr24` is a Python library for data retrieval from [Flightradar24](https://flightradar24.com) using [gRPC](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) and JSON APIs.

For a detailed quickstart, examples and references, please refer to the [documentation](https://cathaypacific8747.github.io/fr24/usage/quickstart/).

## Features

`fr24` supports the following endpoints:

| Endpoint                      | Description                                                    | Type   |
| ------------------------------| -------------------------------------------------------------- | ------ |
| **Live Feed**                 | Current real-time flight data within a bounding box.           | gRPC   |
| **Live Feed Playback**        | Historical snapshot of live feed data for a specific time.     | gRPC   |
| **Flight List**               | List of flights based on registration or flight number.        | JSON   |
| **Playback**                  | Historical state vectors data for a flight.                    | JSON   |
| **Airport Arrivals**          | Aircraft arrival information for a given airport.              | JSON   |
| **Airport Search**            | Search for airports by keyword.                                | JSON   |
| **Nearest Flights**           | Real-time flight data for aircraft within a given radius.      | gRPC   |
| **Follow Flight** (streaming) | Historical track and real-time updates for a live flight.      | gRPC   |
| **Top Flights**               | List of the most viewed flights.                               | gRPC   |

<!--
| **Live Flight Status**        | Real-time status updates for live flights.                     | gRPC   |
| **Live Trail**                | Real-time trail data for a flight.                             | gRPC   |
| **Historic Trail**            | Historical trail data for a flight.                            | gRPC   |
-->

`fr24` is built with modularity and performance in mind, utilising asynchronous programming to handle concurrent requests efficiently.

## Installation

For the latest stable version:

```sh
pip install fr24
```

For a development version, clone the repository and run in the directory:

```sh
uv venv
source .venv/bin/activate
uv sync --all-extras --all-groups
```

This installs all optional dependencies, typing, linting, testing and documentation tools.

## Examples

Fetch live feed data for a specific bounding box:

```py
import asyncio

from fr24 import FR24


async def main() -> None:
    async with FR24() as client:
        result = await client.live_feed.fetch()
        print(result.response.content)  # access raw, undecoded bytes
        # convert to other formats:
        print(result.to_proto())  # protobuf object
        print(result.to_dict())  # nested dictionary
        print(result.to_polars())  # polars dataframe

        # write to a parquet file:
        result.write_table("feed.parquet")


if __name__ == "__main__":
    asyncio.run(main())
```

To improve efficiency and reduce API calls, `fr24` provides a simple file-based cache:

```py
import asyncio

from fr24 import FR24, FR24Cache

cache = FR24Cache.default()

async def main() -> None:
    async with FR24() as client:
        result = await client.live_feed.fetch()
        # on Linux, this writes to ~/.cache/fr24/feed/{timestamp_s}.parquet
        result.write_table(cache)

def some_time_later() -> None:
    for fp in cache.live_feed.glob("*"):
        print(fp)
        print(cache.live_feed.scan_table(fp).collect())

if __name__ == "__main__":
    asyncio.run(main())
    some_time_later()
```

`fr24` also comes with a CLI for quick data retrieval:

```console
$ fr24 feed -o feed.parquet
$ duckdb -c "describe select * from 'feed.parquet'";
┌─────────────────┬───────────────────────────────────────────────────────────────────┬─────────┬─────────┬─────────┬─────────┐
│   column_name   │                            column_type                            │  null   │   key   │ default │  extra  │
│     varchar     │                              varchar                              │ varchar │ varchar │ varchar │ varchar │
├─────────────────┼───────────────────────────────────────────────────────────────────┼─────────┼─────────┼─────────┼─────────┤
│ timestamp       │ UINTEGER                                                          │ YES     │         │         │         │
│ flightid        │ UINTEGER                                                          │ YES     │         │         │         │
│ latitude        │ FLOAT                                                             │ YES     │         │         │         │
│ longitude       │ FLOAT                                                             │ YES     │         │         │         │
│ track           │ USMALLINT                                                         │ YES     │         │         │         │
│ altitude        │ INTEGER                                                           │ YES     │         │         │         │
│ ground_speed    │ SMALLINT                                                          │ YES     │         │         │         │
│ on_ground       │ BOOLEAN                                                           │ YES     │         │         │         │
│ callsign        │ VARCHAR                                                           │ YES     │         │         │         │
│ source          │ UTINYINT                                                          │ YES     │         │         │         │
│ registration    │ VARCHAR                                                           │ YES     │         │         │         │
│ origin          │ VARCHAR                                                           │ YES     │         │         │         │
│ destination     │ VARCHAR                                                           │ YES     │         │         │         │
│ typecode        │ VARCHAR                                                           │ YES     │         │         │         │
│ eta             │ UINTEGER                                                          │ YES     │         │         │         │
│ vertical_speed  │ SMALLINT                                                          │ YES     │         │         │         │
│ squawk          │ USMALLINT                                                         │ YES     │         │         │         │
│ position_buffer │ STRUCT(delta_lat INTEGER, delta_lon INTEGER, delta_ms UINTEGER)[] │ YES     │         │         │         │
├─────────────────┴───────────────────────────────────────────────────────────────────┴─────────┴─────────┴─────────┴─────────┤
│ 18 rows                                                                                                           6 columns │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

For a full list of commands and options, run:

```sh
fr24 --help
```

`fr24` also comes with a TUI - search for flights directly in your terminal:

```sh
fr24 tui
```

## Disclaimer

> [!IMPORTANT]  
> Code has been developed for educational purposes ONLY. Do not abuse it.

```json
{
  "copyright": "Copyright (c) 2014-2025 Flightradar24 AB. All rights reserved.",
  "legalNotice": "The contents of this file and all derived data are the property of Flightradar24 AB for use exclusively by its products and applications. Using, modifying or redistributing the data without the prior written permission of Flightradar24 AB is not allowed and may result in prosecutions."
}
```

Official Flightradar24 API: https://fr24api.flightradar24.com/