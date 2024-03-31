The majority of the core code is developed in a [functional style](./functions.md).

However, the [fr24.core.FR24][] class provides a convenient wrapper around these functions.
Every response is automatically saved into the following directories, relative to the [base cache directory](../usage/cli.md#directories):

- [Flight list][fr24.core.FR24.flight_list]
    - `flight_list/reg/{reg.upper()}.parquet`, or
    - `flight_list/flight/{iata_flight_num.upper()}.parquet`
- [Playback][fr24.core.FR24.playback]
    - `playback/{fr24_hex_id.lower()}.parquet`
- [Live feed][fr24.core.FR24.livefeed]
    - `feed/{timestamp_ms}.parquet`

The current implementation is poor and is being reworked.


::: fr24.core
