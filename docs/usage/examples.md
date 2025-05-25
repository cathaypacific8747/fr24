# Overview


| Name                                                                                  | Core functions                                                                         | Service and Cache Location                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Flight List](#flight-list)<br><span class="chip chip-json">JSON</span>               | [`flight_list`][fr24.json.flight_list]<br>[`flight_list_df`][fr24.json.flight_list_df] | [`FlightListService`][fr24.service.FlightListService]<br><br>Cache Location:<br>`flight_list/`<br>`└── reg/`<br>`​    └── {reg.upper()}.parquet`<br>`└── flight_list/`<br>`​    └── {iata_flight_num.upper()}.parquet` |
| [Playback](#playback)<br><span class="chip chip-json">JSON</span>                     | [`playback`][fr24.json.playback]<br>[`playback_df`][fr24.json.playback_df]             | [`PlaybackService`][fr24.service.PlaybackService]<br><br>Cache Location:<br>`playback/`<br>`└── {fr24_hex_id.lower()}.parquet`                                                                                         |
| [Live Feed](#live-feed)<br><span class="chip chip-grpc">gRPC</span>                   | [`live_feed`][fr24.grpc.live_feed]<br>[`live_feed_df`][fr24.grpc.live_feed_df]         | [`LiveFeedService`][fr24.service.LiveFeedService]<br><br>Cache Location:<br>`feed/`<br>`└── {timestamp_s}.parquet`                                                                                                     |
| [Airport Arrivals](#airport-arrivals)<br><span class="chip chip-json">JSON</span>     | [`airport_list`][fr24.json.airport_list]                                               | -                                                                                                                                                                                                                      |
| [Airport Search](#airport-search)<br><span class="chip chip-json">JSON</span>         | [`find`][fr24.json.find]                                                               | -                                                                                                                                                                                                                      |
| [Nearest Flights](#nearest-flights)<br><span class="chip chip-grpc">gRPC</span>       | [`nearest_flights`][fr24.grpc.nearest_flights]                                         | [`NearestFlightsService`][fr24.service.NearestFlightsService]<br><br>Cache Location:<br>`nearest_flights/`<br>`└── {lon_x1e6}_{lat_x1e6}_{timestamp_s}.parquet`                                                        |
| [Live Flight Status](#live-flight-status)<br><span class="chip chip-grpc">gRPC</span> | [`live_flights_status`][fr24.grpc.live_flights_status]                                 | [`LiveFlightsStatusService`][fr24.service.LiveFlightsStatusService]<br><br>Cache Location:<br>`live_flights_status/`<br>`└── {timestamp_s}.parquet`                                                                    |
| [Follow Flight](#follow-flight)<br><span class="chip chip-grpc">gRPC</span>           | [`follow_flight_stream`][fr24.grpc.follow_flight_stream]                               | -                                                                                                                                                                                                                      |
| [Top Flights](#top-flights)<br><span class="chip chip-grpc">gRPC</span>               | [`top_flights`][fr24.grpc.top_flights]                                                 | -                                                                                                                                                                                                                      |
| [Live Trail](#live-trail)<br><span class="chip chip-grpc">gRPC</span>                 | [`live_trail`][fr24.grpc.live_trail]                                                   | -                                                                                                                                                                                                                      |
| [Flight Details](#flight-details)<br><span class="chip chip-grpc">gRPC</span>         | [`flight_details`][fr24.grpc.flight_details]                                           | -                                                                                                                                                                                                                      |
| [Playback Flight](#playback-flight)<br><span class="chip chip-grpc">gRPC</span>       | [`playback_flight`][fr24.grpc.playback_flight]                                         | -                                                                                                                                                                                                                      |

You can find even more usage examples under [`tests/`](https://github.com/cathaypacific8747/fr24/tree/master/tests).

[Skip to core functions](#core-functions)

## `FR24` class

### Flight list

#### Single page
=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/10_flight_list.py:script0"
    ```

=== "`result.to_polars()`"
    
    ```
    --8<-- "docs/usage/scripts/10_flight_list.py:df0"
    ```

#### Paginate all pages
Queries for next page as long as user doesn't enter `x`, or if there are no pages left.
In each iteration, rows are upserted and saved to the [cache](./directories.md).

Note that pagination cannot be run in parallel: fetching page N requires information from page N-1.

=== "Jupyter cell"

    ```py hl_lines="7 9 13"
    --8<-- "docs/usage/scripts/10_flight_list.py:script1"
    ```

    1. Create a new result collections, a list under the hood.
    2. Appends the current flight list to the collection. Note that it does not remove duplicates.
    3. Merges the collections into a single table. Removes duplicates (if any).

=== "`results.to_polars()`"
    
    ```
    --8<-- "docs/usage/scripts/10_flight_list.py:df1"
    ```

### Playback

#### Miracle on the Hudson
Downloads the flight trajectory for [UA1549](https://en.wikipedia.org/wiki/US_Airways_Flight_1549)

=== "Jupyter cell"

    ```py hl_lines="6"
    --8<-- "docs/usage/scripts/11_playback.py:script0"
    ```

    1. From https://www.flightradar24.com/data/pinned/ua1549-2fb3041#2fb3041.

=== "`data.df`"
    
    ```
    --8<-- "docs/usage/scripts/11_playback.py:df0"
    ```

=== "`data.metadata`"
    
    ```py
    --8<-- "docs/usage/scripts/11_playback.py:metadata0"
    ```

#### File operations
Saves trajectory data to disk, reads the track and metadata from it.

=== "Jupyter cell"

    ```py hl_lines="9 11"
    --8<-- "docs/usage/scripts/11_playback.py:script1"
    ```
    
    1. Saves the parquet to the [cache](./directories.md).
    2. Load the parquet from the [cache](./directories.md).

=== "`data_local.df`"
    
    ```
    --8<-- "docs/usage/scripts/11_playback.py:df0"
    ```

=== "`data_local.metadata`"
    
    ```py
    --8<-- "docs/usage/scripts/11_playback.py:metadata0"
    ```
### Live Feed

#### Live
This example is covered in detail in the [quickstart](./quickstart.md).

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/12_live_feed.py:script"
    ```

=== "`result`"
    
    ```py
    --8<-- "docs/usage/scripts/12_live_feed.py:result"
    ```

=== "`result.to_dict()`"
    
    ```py
    --8<-- "docs/usage/scripts/12_live_feed.py:dict"
    ```

=== "`result.to_polars()`"
    
    ```
    --8<-- "docs/usage/scripts/12_live_feed.py:polars"
    ```

#### Playback
Fetches the live feed three days ago.

=== "Jupyter cell"

    ```py hl_lines="4"
    --8<-- "docs/usage/scripts/12_live_feed.py:script2"
    ```

=== "`result.to_polars()`"
    
    ```
    --8<-- "docs/usage/scripts/12_live_feed.py:polars2"
    ```

### Nearest Flights

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/13_nearest_flights.py:script"
    ```

=== "`result`"
    
    ```py
    --8<-- "docs/usage/scripts/13_nearest_flights.py:result"
    ```

=== "`result.to_dict()`"
    
    ```py
    --8<-- "docs/usage/scripts/13_nearest_flights.py:dict"
    ```

=== "`result.to_polars()`"
    
    ```
    --8<-- "docs/usage/scripts/13_nearest_flights.py:polars"
    ```

### Live Flights Status

Retrieve the flight status for the closest flights from a location

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/14_live_flights_status.py:script"
    ```

=== "`result`"
    
    ```py
    --8<-- "docs/usage/scripts/14_live_flights_status.py:result"
    ```

=== "`result.to_dict()`"
    
    ```py
    --8<-- "docs/usage/scripts/14_live_flights_status.py:dict"
    ```

=== "`result.to_polars()`"
    
    ```
    --8<-- "docs/usage/scripts/14_live_flights_status.py:polars"
    ```

## Core functions
### Flight list

=== "Jupyter cell"

    ```py hl_lines="17"
    --8<-- "docs/usage/scripts/20_flight_list.py:script0"
    ```

    1. Replace it with the current time.

=== "`df`"
    
    ```
    --8<-- "docs/usage/scripts/20_flight_list.py:df0"
    ```

### Playback

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/21_playback.py:script0"
    ```

=== "`df`"
    
    ```
    --8<-- "docs/usage/scripts/21_playback.py:df0"
    ```

### Airport Arrivals

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/22_arrivals.py:script0"
    ```

=== "`df`"
    
    ```
    --8<-- "docs/usage/scripts/22_arrivals.py:df0"
    ```

### Airport Search

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/23_find.py:script0"
    ```

=== "`df`"
    
    ```
    --8<-- "docs/usage/scripts/23_find.py:df0"
    ```

### Live feed

Demonstrates custom bounding boxes.

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/24_live_feed.py:script0"
    ```

    1. The type is a `Result[LiveFeedResponse, ProtoError]`, calling the `.unwrap()` method raises an exception if there is an error.

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/24_live_feed.py:output0"
    ```

In JSON format:

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/24_live_feed.py:script1"
    ```

=== "Output"
    
    ```py
    --8<-- "docs/usage/scripts/24_live_feed.py:output1"
    ```

### Nearest Flights

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/25_nearest_flights.py:script0"
    ```

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/25_nearest_flights.py:output0"
    ```

### Live Flight Status

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/26_live_flights_status.py:script0"
    ```

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/26_live_flights_status.py:output0"
    ```

### Follow Flight

!!! tip
    This is a streaming API that repeatedly updates the aircraft state vectors.

    Initial metadata (`aircraft_info`, `flight_plan` and `flight_trail_list`)
    is only sent in the first packet of data.

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/28_follow_flight.py:script0"
    ```

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/28_follow_flight.py:output0"
    ```

### Top Flights

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/29_top_flights.py:script0"
    ```

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/29_top_flights.py:output0"
    ```

### Live Trail

!!! warning
    Unstable API - does not return data reliably.

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/30_live_trail.py:script0"
    ```

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/30_live_trail.py:output0"
    ```

### Flight Details

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/32_flight_details.py:script0"
    ```

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/32_flight_details.py:output0"
    ```


### Playback Flight

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/33_playback_flight.py:script0"
    ```

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/33_playback_flight.py:output0"
    ```