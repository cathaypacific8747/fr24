Most of the core code is developed in a functional style, though the [fr24.core.FR24][] class provides a wrapper around them. Every response is automatically saved into the following directories:

- Feed
    - `feed/playback/{timestamp_ms}.parquet`
    - `feed/live/{timestmap_ms}.parquet`
- Flight history
    - `flight_list/reg/{reg}.parquet`, or
    - `flight_list/flight/{iata_flight_num}.parquet`
- Playback
    - `playback/metadata/{fr24_id}.parquet`
    - `playback/track/{fr24_id}.parquet`
    - `playback/track_ems/{fr24_id}.parquet`

Note that the fr24 flight ID is in base 10, not hex.

The current implementation is poor and is being reworked.

::: fr24.livefeed
::: fr24.history
::: fr24.find
::: fr24.authentication
::: fr24.core
