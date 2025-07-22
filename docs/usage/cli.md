# CLI
List all commands and show help:

=== "Shell"

    ```command
    fr24 --help
    ```

=== "Output"
    
    ```
                                                                                    
    Usage: fr24 [OPTIONS] COMMAND [ARGS]...                                        
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --install-completion          Install completion for the current shell.      │
    │ --show-completion             Show completion for the current shell, to copy │
    │                               it or customize the installation.              │
    │ --help                        Show this message and exit.                    │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────╮
    │ dirs          Shows relevant directories                                     │
    │ tui           Starts the TUI                                                 │
    │ feed          Fetches current (or playback of) live feed at a given time     │
    │ flight-list   Fetches flight list for the given registration or flight       │
    │               number                                                         │
    │ playback      Fetches historical track playback data for the given flight    │
    │ auth          Commands for authentication                                    │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ```

Dump the current (or playback of) live feed:

=== "Shell"

    ```command
    fr24 feed --help
    fr24 feed
    fr24 feed --timestamp 2023-12-17T18:56:00
    fr24 feed -o feed.parquet
    fr24 feed --format csv -o - > feed.csv
    ```

=== "Output"

    ```command
    $ fr24 feed --help
                                                                                
    Usage: fr24 feed [OPTIONS]                                                     
                                                                                    
    Fetches current (or playback of) live feed at a given time                     
                                                                                    
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --timestamp          TEXT           Time of the snapshot (optional), an ISO  │
    │                                     8601 format input (e.g.                  │
    │                                     2024-06-04T00:00:00). Live data will be  │
    │                                     fetched if not provided.                 │
    │                                     [default: now]                           │
    │ --output     -o      FILE           Save results as parquet to a specific    │
    │                                     filepath. If `-`, results will be        │
    │                                     printed to stdout.                       │
    │                                     [default: None]                          │
    │ --format     -f      [parquet|csv]  Output format, `parquet` or `csv`        │
    │                                     [default: parquet]                       │
    │ --help                              Show this message and exit.              │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    $ fr24 feed -o feed.parquet
    success: wrote 831 rows to /home/cx/projects/research/fr24/feed.parquet.
    Preview:
    shape: (5, 18)
    ┌─────────┬─────────┬─────────┬─────────┬───┬─────┬────────┬─────────┬─────────┐
    │ timesta ┆ flighti ┆ latitud ┆ longitu ┆ … ┆ eta ┆ squawk ┆ vertica ┆ positio │
    │ mp      ┆ d       ┆ e       ┆ de      ┆   ┆ --- ┆ ---    ┆ l_speed ┆ n_buffe │
    │ ---     ┆ ---     ┆ ---     ┆ ---     ┆   ┆ u32 ┆ u16    ┆ ---     ┆ r       │
    │ datetim ┆ u32     ┆ f32     ┆ f32     ┆   ┆     ┆        ┆ i16     ┆ ---     │
    │ e[ms,   ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ list    ┆
    ┆         ┆         ┆   ┆     ┆        ┆         ┆ ruct[3] │
    │         ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ ]       │
    ╞═════════╪═════════╪═════════╪═════════╪═══╪═════╪════════╪═════════╪═════════╡
    │ 2025-07 ┆ 9957282 ┆ 42.1415 ┆ -3.1932 ┆ … ┆ 0   ┆ 0      ┆ 0       ┆ [{251,6 │
    │ -21 05: ┆ 88      ┆ 86      ┆ 76      ┆   ┆     ┆        ┆         ┆ ,1310}, │
    │ 02:40.2 ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ {462,12 │
    │ 72 UTC  ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ ,2370}, │
    │         ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ …       │
    │ 2025-07 ┆ 9957278 ┆ 42.4208 ┆ -3.7603 ┆ … ┆ 0   ┆ 0      ┆ 0       ┆ [{186,- │
    │ -21 05: ┆ 52      ┆ 18      ┆ 9       ┆   ┆     ┆        ┆         ┆ 19,991} │
    │ 02:39.2 ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ , {365, │
    │ 25 UTC  ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ -44,194 │
    │         ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ 5}…     │
    │ 2025-07 ┆ 9956879 ┆ 42.3423 ┆ -2.6387 ┆ … ┆ 0   ┆ 0      ┆ 0       ┆ [{160,1 │
    │ -21 05: ┆ 03      ┆ 16      ┆ 16      ┆   ┆     ┆        ┆         ┆ 31,860} │
    │ 02:39.8 ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ , {417, │
    │ 33 UTC  ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ 336,221 │
    │         ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ 5}…     │
    │ 2025-07 ┆ 9957283 ┆ 42.2023 ┆ -2.9734 ┆ … ┆ 0   ┆ 0      ┆ 0       ┆ [{179,9 │
    │ -21 05: ┆ 13      ┆ 77      ┆ 87      ┆   ┆     ┆        ┆         ┆ 9,980}, │
    │ 02:39.3 ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ {357,19 │
    │ 99 UTC  ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ 9,1900} │
    │         ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ ,…      │
    │ 2025-07 ┆ 9957204 ┆ 42.4984 ┆ -7.3180 ┆ … ┆ 0   ┆ 0      ┆ 0       ┆ [{-393, │
    │ -21 05: ┆ 57      ┆ 59      ┆ 18      ┆   ┆     ┆        ┆         ┆ -449,24 │
    │ 02:40.6 ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ 80},    │
    │ 26 UTC  ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ {-480,- │
    │         ┆         ┆         ┆         ┆   ┆     ┆        ┆         ┆ 546,…   │
    └─────────┴─────────┴─────────┴─────────┴───┴─────┴────────┴─────────┴─────────┘

    $ duckdb -c "describe select * from 'feed.parquet';"
    ┌─────────────────┬──────────────────────┬─────────┬───┬─────────┬─────────┐
    │   column_name   │     column_type      │  null   │ … │ default │  extra  │
    │     varchar     │       varchar        │ varchar │   │ varchar │ varchar │
    ├─────────────────┼──────────────────────┼─────────┼───┼─────────┼─────────┤
    │ timestamp       │ TIMESTAMP WITH TIM…  │ YES     │ … │ NULL    │ NULL    │
    │ flightid        │ UINTEGER             │ YES     │ … │ NULL    │ NULL    │
    │ latitude        │ FLOAT                │ YES     │ … │ NULL    │ NULL    │
    │ longitude       │ FLOAT                │ YES     │ … │ NULL    │ NULL    │
    │ track           │ USMALLINT            │ YES     │ … │ NULL    │ NULL    │
    │ altitude        │ INTEGER              │ YES     │ … │ NULL    │ NULL    │
    │ ground_speed    │ SMALLINT             │ YES     │ … │ NULL    │ NULL    │
    │ on_ground       │ BOOLEAN              │ YES     │ … │ NULL    │ NULL    │
    │ callsign        │ VARCHAR              │ YES     │ … │ NULL    │ NULL    │
    │ source          │ UTINYINT             │ YES     │ … │ NULL    │ NULL    │
    │ registration    │ VARCHAR              │ YES     │ … │ NULL    │ NULL    │
    │ origin          │ VARCHAR              │ YES     │ … │ NULL    │ NULL    │
    │ destination     │ VARCHAR              │ YES     │ … │ NULL    │ NULL    │
    │ typecode        │ VARCHAR              │ YES     │ … │ NULL    │ NULL    │
    │ eta             │ UINTEGER             │ YES     │ … │ NULL    │ NULL    │
    │ squawk          │ USMALLINT            │ YES     │ … │ NULL    │ NULL    │
    │ vertical_speed  │ SMALLINT             │ YES     │ … │ NULL    │ NULL    │
    │ position_buffer │ STRUCT(delta_lat I…  │ YES     │ … │ NULL    │ NULL    │
    ├─────────────────┴──────────────────────┴─────────┴───┴─────────┴─────────┤
    │ 18 rows                                              6 columns (5 shown) │
    └──────────────────────────────────────────────────────────────────────────┘
    ```

Dump the flight list for a given registration or flight number

=== "Shell"

    ```
    fr24 flight-list --help
    fr24 flight-list --reg B-HPB
    fr24 flight-list --flight CX488
    fr24 flight-list --flight CX488 --all
    fr24 flight-list --reg B-HPB -o flight-list.parquet
    fr24 flight-list --reg B-HPB --format csv -o - > flight-list.csv
    ```

=== "Output"

    ```command
    $ fr24 flight-list --help
                                                                                    
    Usage: fr24 flight-list [OPTIONS]                                              
                                                                                    
    Fetches flight list for the given registration or flight number                
                                                                                    
                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --reg                TEXT           Aircraft registration (e.g. B-HUJ)       │
    │                                     [default: None]                          │
    │ --flight             TEXT           Flight number (e.g. CX8747)              │
    │                                     [default: None]                          │
    │ --timestamp          TEXT           Show flights with ATD before this time   │
    │                                     (optional), an ISO 8601 format input     │
    │                                     (e.g. 2024-06-04T00:00:00)               │
    │                                     [default: now]                           │
    │ --all                               Get all pages of flight list             │
    │ --output     -o      FILE           Save results as parquet to a specific    │
    │                                     filepath. If `-`, results will be        │
    │                                     printed to stdout.                       │
    │                                     [default: None]                          │
    │ --format     -f      [parquet|csv]  Output format, `parquet` or `csv`        │
    │                                     [default: parquet]                       │
    │ --help                              Show this message and exit.              │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    $ fr24 flight-list --reg B-HPB -o flight-list.parquet
    success: wrote 10 rows to /path/to/flight-list.parquet.
    Preview:
    shape: (5, 15)
    ┌─────────┬────────┬─────────┬─────────┬───┬────────┬────────┬────────┬────────┐
    │ flight_ ┆ number ┆ callsig ┆ icao24  ┆ … ┆ ATOD   ┆ STOA   ┆ ETOA   ┆ ATOA   │
    │ id      ┆ ---    ┆ n       ┆ ---     ┆   ┆ ---    ┆ ---    ┆ ---    ┆ ---    │
    │ ---     ┆ str    ┆ ---     ┆ u32     ┆   ┆ dateti ┆ dateti ┆ dateti ┆ dateti │
    │ u64     ┆        ┆ str     ┆         ┆   ┆ me[ms, ┆ me[ms, ┆ me[ms, ┆ me   ┆ 
    UTC]   ┆ UTC]   ┆ UTC]   │
    ╞═════════╪════════╪═════════╪═════════╪═══╪════════╪════════╪════════╪════════╡
    │ 9957006 ┆ CX928  ┆ CPA928  ┆ 7901768 ┆ … ┆ 2025-0 ┆ 2025-0 ┆ null   ┆ 2025-0 │
    │ 10      ┆        ┆         ┆         ┆   ┆ 7-21   ┆ 7-21   ┆        ┆ 7-21   │
    │         ┆        ┆         ┆         ┆   ┆ 00:37: ┆ 03:00: ┆        ┆ 02:32: │
    │         ┆        ┆         ┆         ┆   ┆ 42 UTC ┆ 00 UTC ┆        ┆ 57 UTC │
    │ 9956018 ┆ CX963  ┆ null    ┆ 7901768 ┆ … ┆ 2025-0 ┆ 2025-0 ┆ null   ┆ 2025-0 │
    │ 61      ┆        ┆         ┆         ┆   ┆ 7-20   ┆ 7-20   ┆        ┆ 7-20   │
    │         ┆        ┆         ┆         ┆   ┆ 15:13: ┆ 14:20: ┆        ┆ 17:05: │
    │         ┆        ┆         ┆         ┆   ┆ 19 UTC ┆ 00 UTC ┆        ┆ 43 UTC │
    │ 9955613 ┆ CX962  ┆ CPA962  ┆ 7901768 ┆ … ┆ 2025-0 ┆ 2025-0 ┆ null   ┆ 2025-0 │
    │ 60      ┆        ┆         ┆         ┆   ┆ 7-20   ┆ 7-20   ┆        ┆ 7-20   │
    │         ┆        ┆         ┆         ┆   ┆ 11:53: ┆ 10:20: ┆        ┆ 13:40: │
    │         ┆        ┆         ┆         ┆   ┆ 31 UTC ┆ 00 UTC ┆        ┆ 04 UTC │
    │ 9953866 ┆ CX989  ┆ CPA989  ┆ 7901768 ┆ … ┆ 2025-0 ┆ 2025-0 ┆ null   ┆ 2025-0 │
    │ 18      ┆        ┆         ┆         ┆   ┆ 7-19   ┆ 7-19   ┆        ┆ 7-19   │
    │         ┆        ┆         ┆         ┆   ┆ 16:05: ┆ 15:40: ┆        ┆ 16:56: │
    │         ┆        ┆         ┆         ┆   ┆ 28 UTC ┆ 00 UTC ┆        ┆ 36 UTC │
    │ 9953446 ┆ CX988  ┆ CPA988  ┆ 7901768 ┆ … ┆ 2025-0 ┆ 2025-0 ┆ null   ┆ 2025-0 │
    │ 82      ┆        ┆         ┆         ┆   ┆ 7-19   ┆ 7-19   ┆        ┆ 7-19   │
    │         ┆        ┆         ┆         ┆   ┆ 13:47: ┆ 13:05: ┆        ┆ 14:24: │
    │         ┆        ┆         ┆         ┆   ┆ 01 UTC ┆ 00 UTC ┆        ┆ 19 UTC │
    └─────────┴────────┴─────────┴─────────┴───┴────────┴────────┴────────┴────────┘

    $ duckdb -c "describe select * from 'flight-list.parquet';"
    ┌──────────────┬───────────────────────┬─────────┬─────────┬─────────┬─────────┐
    │ column_name  │      column_type      │  null   │   key   │ default │  extra  │
    │   varchar    │        varchar        │ varchar │ varchar │ varchar │ varchar │
    ├──────────────┼───────────────────────┼─────────┼─────────┼─────────┼─────────┤
    │ flight_id    │ UBIGINT               │ YES     │ NULL    │ NULL    │ NULL    │
    │ number       │ VARCHAR               │ YES     │ NULL    │ NULL    │ NULL    │
    │ callsign     │ VARCHAR               │ YES     │ NULL    │ NULL    │ NULL    │
    │ icao24       │ UINTEGER              │ YES     │ NULL    │ NULL    │ NULL    │
    │ registration │ VARCHAR               │ YES     │ NULL    │ NULL    │ NULL    │
    │ typecode     │ VARCHAR               │ YES     │ NULL    │ NULL    │ NULL    │
    │ origin       │ VARCHAR               │ YES     │ NULL    │ NULL    │ NULL    │
    │ destination  │ VARCHAR               │ YES     │ NULL    │ NULL    │ NULL    │
    │ status       │ VARCHAR               │ YES     │ NULL    │ NULL    │ NULL    │
    │ STOD         │ TIMESTAMP WITH TIME…  │ YES     │ NULL    │ NULL    │ NULL    │
    │ ETOD         │ TIMESTAMP WITH TIME…  │ YES     │ NULL    │ NULL    │ NULL    │
    │ ATOD         │ TIMESTAMP WITH TIME…  │ YES     │ NULL    │ NULL    │ NULL    │
    │ STOA         │ TIMESTAMP WITH TIME…  │ YES     │ NULL    │ NULL    │ NULL    │
    │ ETOA         │ TIMESTAMP WITH TIME…  │ YES     │ NULL    │ NULL    │ NULL    │
    │ ATOA         │ TIMESTAMP WITH TIME…  │ YES     │ NULL    │ NULL    │ NULL    │
    ├──────────────┴───────────────────────┴─────────┴─────────┴─────────┴─────────┤
    │ 15 rows                                                            6 columns │
    └──────────────────────────────────────────────────────────────────────────────┘
    ```

Dump the historical track playback data for the given flight

=== "Shell"

    ```
    fr24 playback --help
    fr24 playback 2d81a27
    fr24 playback 2d81a27 -o playback.parquet
    fr24 playback 2d81a27 --format csv -o - > playback.csv
    ```

=== "Output"

    ```command
    $ fr24 playback --help
                                                                                    
    Usage: fr24 playback [OPTIONS] FLIGHT_ID                                       
                                                                                    
    Fetches historical track playback data for the given flight                    
                                                                                    
    ╭─ Arguments ──────────────────────────────────────────────────────────────────╮
    │ *    flight_id      TEXT  Hex Flight ID (e.g. `2d81a27`, `0x2d81a27`)        │
    │                           [default: None]                                    │
    │                           [required]                                         │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --timestamp          TEXT           ATD (optional), an ISO 8601 format input │
    │                                     (e.g. 2024-06-04T00:00:00)               │
    │                                     [default: None]                          │
    │ --output     -o      FILE           Save results as parquet to a specific    │
    │                                     filepath. If `-`, results will be        │
    │                                     printed to stdout.                       │
    │                                     [default: None]                          │
    │ --format     -f      [parquet|csv]  Output format, `parquet` or `csv`        │
    │                                     [default: parquet]                       │
    │ --help                              Show this message and exit.              │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    $ fr24 playback 2d81a27 -o playback.parquet
    success: wrote 62 rows to /path/to/playback.parquet.
    Preview:
    shape: (5, 9)
    ┌─────────┬─────────┬─────────┬─────────┬───┬────────┬───────┬────────┬────────┐
    │ timesta ┆ latitud ┆ longitu ┆ altitud ┆ … ┆ vertic ┆ track ┆ squawk ┆ ems    │
    │ mp      ┆ e       ┆ de      ┆ e       ┆   ┆ al_spe ┆ ---   ┆ ---    ┆ ---    │
    │ ---     ┆ ---     ┆ ---     ┆ ---     ┆   ┆ ed     ┆ i16   ┆ u16    ┆ struct │
    │ u32     ┆ f32     ┆ f32     ┆ i32     ┆   ┆ ---    ┆       ┆        ┆ [18]   │
    │         ┆         ┆         ┆         ┆   ┆ i16    ┆       ┆        ┆        │
    ╞═════════╪═════════╪═════════╪═════════╪═══╪════════╪═══════╪════════╪════════╡
    │ 1394210 ┆ 2.7983  ┆ 101.689 ┆ 1500    ┆ … ┆ null   ┆ 328   ┆ 1135   ┆ null   │
    │ 550     ┆         ┆ 003     ┆         ┆   ┆        ┆       ┆        ┆        │
    │ 1394210 ┆ 2.80333 ┆ 101.685 ┆ 1575    ┆ … ┆ null   ┆ 327   ┆ 1135   ┆ null   │
    │ 557     ┆         ┆ 997     ┆         ┆   ┆        ┆       ┆        ┆        │
    │ 1394210 ┆ 2.80838 ┆ 101.682 ┆ 1650    ┆ … ┆ null   ┆ 327   ┆ 1135   ┆ null   │
    │ 563     ┆         ┆ 999     ┆         ┆   ┆        ┆       ┆        ┆        │
    │ 1394210 ┆ 2.81292 ┆ 101.68  ┆ 1725    ┆ … ┆ null   ┆ 327   ┆ 1135   ┆ null   │
    │ 570     ┆         ┆         ┆         ┆   ┆        ┆       ┆        ┆        │
    │ 1394210 ┆ 2.81841 ┆ 101.676 ┆ 1825    ┆ … ┆ null   ┆ 327   ┆ 1135   ┆ null   │
    │ 576     ┆         ┆ 003     ┆         ┆   ┆        ┆       ┆        ┆        │
    └─────────┴─────────┴─────────┴─────────┴───┴────────┴───────┴────────┴────────┘

    $ duckdb -c "describe select * from 'playback.parquet';"
    ┌────────────────┬──────────────────────┬─────────┬───┬─────────┬─────────┐
    │  column_name   │     column_type      │  null   │ … │ default │  extra  │
    │    varchar     │       varchar        │ varchar │   │ varchar │ varchar │
    ├────────────────┼──────────────────────┼─────────┼───┼─────────┼─────────┤
    │ timestamp      │ UINTEGER             │ YES     │ … │ NULL    │ NULL    │
    │ latitude       │ FLOAT                │ YES     │ … │ NULL    │ NULL    │
    │ longitude      │ FLOAT                │ YES     │ … │ NULL    │ NULL    │
    │ altitude       │ INTEGER              │ YES     │ … │ NULL    │ NULL    │
    │ ground_speed   │ SMALLINT             │ YES     │ … │ NULL    │ NULL    │
    │ vertical_speed │ SMALLINT             │ YES     │ … │ NULL    │ NULL    │
    │ track          │ SMALLINT             │ YES     │ … │ NULL    │ NULL    │
    │ squawk         │ USMALLINT            │ YES     │ … │ NULL    │ NULL    │
    │ ems            │ STRUCT("timestamp"…  │ YES     │ … │ NULL    │ NULL    │
    ├────────────────┴──────────────────────┴─────────┴───┴─────────┴─────────┤
    │ 9 rows                                              6 columns (5 shown) │
    └─────────────────────────────────────────────────────────────────────────┘
    
    $ duckdb -c "describe select unnest(ems) from 'playback.parquet';"
    ┌──────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
    │ column_name  │ column_type │  null   │   key   │ default │  extra  │
    │   varchar    │   varchar   │ varchar │ varchar │ varchar │ varchar │
    ├──────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
    │ timestamp    │ UINTEGER    │ YES     │ NULL    │ NULL    │ NULL    │
    │ ias          │ SMALLINT    │ YES     │ NULL    │ NULL    │ NULL    │
    │ tas          │ SMALLINT    │ YES     │ NULL    │ NULL    │ NULL    │
    │ mach         │ SMALLINT    │ YES     │ NULL    │ NULL    │ NULL    │
    │ mcp          │ INTEGER     │ YES     │ NULL    │ NULL    │ NULL    │
    │ fms          │ INTEGER     │ YES     │ NULL    │ NULL    │ NULL    │
    │ autopilot    │ TINYINT     │ YES     │ NULL    │ NULL    │ NULL    │
    │ oat          │ TINYINT     │ YES     │ NULL    │ NULL    │ NULL    │
    │ track        │ FLOAT       │ YES     │ NULL    │ NULL    │ NULL    │
    │ roll         │ FLOAT       │ YES     │ NULL    │ NULL    │ NULL    │
    │ qnh          │ USMALLINT   │ YES     │ NULL    │ NULL    │ NULL    │
    │ wind_dir     │ SMALLINT    │ YES     │ NULL    │ NULL    │ NULL    │
    │ wind_speed   │ SMALLINT    │ YES     │ NULL    │ NULL    │ NULL    │
    │ precision    │ UTINYINT    │ YES     │ NULL    │ NULL    │ NULL    │
    │ altitude_gps │ INTEGER     │ YES     │ NULL    │ NULL    │ NULL    │
    │ emergency    │ UTINYINT    │ YES     │ NULL    │ NULL    │ NULL    │
    │ tcas_acas    │ UTINYINT    │ YES     │ NULL    │ NULL    │ NULL    │
    │ heading      │ USMALLINT   │ YES     │ NULL    │ NULL    │ NULL    │
    ├──────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
    │ 18 rows                                                  6 columns │
    └────────────────────────────────────────────────────────────────────┘
    ```

TUI:

```
fr24 tui
```
