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
    │ auth          Commands for authentication                                    │
    │ dirs          Shows relevant directories                                     │
    │ feed          Fetches current (or playback of) live feed at a given time     │
    │ flight-list   Fetches flight list for the given registration or flight       │
    │               number                                                         │
    │ playback      Fetches historical track playback data for the given flight    │
    │ tui           Starts the TUI                                                 │
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
    │ --timestamp          TEXT  Time of the snapshot (optional), a                │
    │                            pd.Timestamp-supported input (e.g.                │
    │                            2024-06-04T00:00:00). Live data will be fetched   │
    │                            if not provided.                                  │
    │                            [default: None]                                   │
    │ --output     -o      FILE  Save results as parquet to a specific filepath.   │
    │                            If `-`, results will be printed to stdout.        │
    │                            [default: None]                                   │
    │ --format     -f      TEXT  Output format, `parquet` or `csv`                 │
    │                            [default: parquet]                                │
    │ --help                     Show this message and exit.                       │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    $ fr24 feed -o feed.parquet
    Success: wrote 13203 rows (977555 bytes) to /home/user/feed.parquet.
    Preview:
            timestamp   flightid   latitude  ...  eta  vertical_speed  squawk
    0      1719299644  903268975 -55.104115  ...    0               0       0
    1      1719299640  903241011  12.738794  ...    0               0       0
    2      1719299640  903274343  -8.169031  ...    0               0       0
    3      1719299644  903291574 -25.104246  ...    0               0       0
    4      1719299644  903256822 -10.495483  ...    0               0       0
    ...           ...        ...        ...  ...  ...             ...     ...
    13198  1719299644  903286908  54.931980  ...    0               0       0
    13199  1719299643  903251738  64.749939  ...    0               0       0
    13200  1719299636  903281352  56.771660  ...    0               0       0
    13201  1719299644  903288803  56.406754  ...    0               0       0
    13202  1719299636  903274725  59.058872  ...    0               0       0

    [13203 rows x 17 columns]

    $ duckdb -c "describe select * from 'feed.parquet';"
    ┌────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
    │  column_name   │ column_type │  null   │   key   │ default │  extra  │
    │    varchar     │   varchar   │ varchar │ varchar │ varchar │ varchar │
    ├────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
    │ timestamp      │ UINTEGER    │ YES     │         │         │         │
    │ flightid       │ UINTEGER    │ YES     │         │         │         │
    │ latitude       │ FLOAT       │ YES     │         │         │         │
    │ longitude      │ FLOAT       │ YES     │         │         │         │
    │ track          │ USMALLINT   │ YES     │         │         │         │
    │ altitude       │ INTEGER     │ YES     │         │         │         │
    │ ground_speed   │ SMALLINT    │ YES     │         │         │         │
    │ on_ground      │ BOOLEAN     │ YES     │         │         │         │
    │ callsign       │ VARCHAR     │ YES     │         │         │         │
    │ source         │ UTINYINT    │ YES     │         │         │         │
    │ registration   │ VARCHAR     │ YES     │         │         │         │
    │ origin         │ VARCHAR     │ YES     │         │         │         │
    │ destination    │ VARCHAR     │ YES     │         │         │         │
    │ typecode       │ VARCHAR     │ YES     │         │         │         │
    │ eta            │ UINTEGER    │ YES     │         │         │         │
    │ vertical_speed │ SMALLINT    │ YES     │         │         │         │
    │ squawk         │ USMALLINT   │ YES     │         │         │         │
    ├────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
    │ 17 rows                                                    6 columns │
    └──────────────────────────────────────────────────────────────────────┘
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
    │ --reg                TEXT  Aircraft registration (e.g. B-HUJ)                │
    │                            [default: None]                                   │
    │ --flight             TEXT  Flight number (e.g. CX8747) [default: None]       │
    │ --timestamp          TEXT  Show flights with ATD before this time            │
    │                            (optional), a pd.Timestamp-supported input (e.g.  │
    │                            2024-06-04T00:00:00)                              │
    │                            [default: now]                                    │
    │ --all                      Get all pages of flight list                      │
    │ --output     -o      FILE  Save results as parquet to a specific filepath.   │
    │                            If `-`, results will be printed to stdout.        │
    │                            [default: None]                                   │
    │ --format     -f      TEXT  Output format, `parquet` or `csv`                 │
    │                            [default: parquet]                                │
    │ --help                     Show this message and exit.                       │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    $ fr24 flight-list --reg B-HPB -o flight-list.parquet
    Success: wrote 10 rows (1284 bytes) to /home/user/flight-list.parquet.
    Preview:
    flight_id number callsign  ...                STOA ETOA                ATOA
    0  903287789  CX740   CPA740  ... 2024-06-25 06:00:00  NaT 2024-06-25 06:03:45
    1  903258455  CX741   CPA741  ... 2024-06-25 02:55:00  NaT 2024-06-25 03:03:05
    2  903220233  CX976   CPA976  ... 2024-06-24 23:40:00  NaT 2024-06-24 23:23:07
    3  903076265  CX913   CPA913  ... 2024-06-24 14:55:00  NaT 2024-06-24 14:43:22
    4  902956726  CX976   CPA976  ... 2024-06-23 23:40:00  NaT 2024-06-23 23:41:52
    5  902846134  CX913   CPA913  ... 2024-06-23 14:55:00  NaT 2024-06-23 15:11:38
    6  902775946  CX439   CPA439  ... 2024-06-23 08:25:00  NaT 2024-06-23 08:18:22
    7  902740251  CX434   CPA434  ... 2024-06-23 03:35:00  NaT 2024-06-23 03:25:48
    8  902529354  CX385   CPA385  ... 2024-06-22 06:00:00  NaT 2024-06-22 06:01:42
    9  902502853  CX384   CPA384  ... 2024-06-22 02:50:00  NaT 2024-06-22 03:18:45

    [10 rows x 15 columns]

    $ duckdb -c "describe select * from 'flight-list.parquet';"
    ┌──────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
    │ column_name  │ column_type │  null   │   key   │ default │  extra  │
    │   varchar    │   varchar   │ varchar │ varchar │ varchar │ varchar │
    ├──────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
    │ flight_id    │ UBIGINT     │ YES     │         │         │         │
    │ number       │ VARCHAR     │ YES     │         │         │         │
    │ callsign     │ VARCHAR     │ YES     │         │         │         │
    │ icao24       │ UINTEGER    │ YES     │         │         │         │
    │ registration │ VARCHAR     │ YES     │         │         │         │
    │ typecode     │ VARCHAR     │ YES     │         │         │         │
    │ origin       │ VARCHAR     │ YES     │         │         │         │
    │ destination  │ VARCHAR     │ YES     │         │         │         │
    │ status       │ VARCHAR     │ YES     │         │         │         │
    │ STOD         │ TIMESTAMP   │ YES     │         │         │         │
    │ ETOD         │ TIMESTAMP   │ YES     │         │         │         │
    │ ATOD         │ TIMESTAMP   │ YES     │         │         │         │
    │ STOA         │ TIMESTAMP   │ YES     │         │         │         │
    │ ETOA         │ TIMESTAMP   │ YES     │         │         │         │
    │ ATOA         │ TIMESTAMP   │ YES     │         │         │         │
    ├──────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
    │ 15 rows                                                  6 columns │
    └────────────────────────────────────────────────────────────────────┘
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
    │ --timestamp          TEXT  ATD (optional), a pd.Timestamp-supported input    │
    │                            (e.g. 2024-06-04T00:00:00)                        │
    │                            [default: None]                                   │
    │ --output     -o      FILE  Save results as parquet to a specific filepath.   │
    │                            If `-`, results will be printed to stdout.        │
    │                            [default: None]                                   │
    │ --format     -f      TEXT  Output format, `parquet` or `csv`                 │
    │                            [default: parquet]                                │
    │ --help                     Show this message and exit.                       │
    ╰──────────────────────────────────────────────────────────────────────────────╯

    $ fr24 playback 2d81a27 -o playback.parquet
    Success: wrote 62 rows (4162 bytes) to /home/user/playback.parquet.
    Preview:
        timestamp  latitude   longitude  ...  track  squawk   ems
    0   1394210550   2.79830  101.689003  ...    328    1135  None
    1   1394210557   2.80333  101.685997  ...    327    1135  None
    2   1394210563   2.80838  101.682999  ...    327    1135  None
    3   1394210570   2.81292  101.680000  ...    327    1135  None
    4   1394210576   2.81841  101.676003  ...    327    1135  None
    ..         ...       ...         ...  ...    ...     ...   ...
    57  1394212757   6.78333  103.512001  ...     25    1135  None
    58  1394212768   6.80000  103.519997  ...     25    1135  None
    59  1394212818   6.90314  103.570000  ...     28    1135  None
    60  1394212835   6.93000  103.589996  ...     40    1135  None
    61  1394212863   6.97000  103.629997  ...     40    1135  None

    [62 rows x 9 columns]

    $ duckdb -c "describe select * from 'playback.parquet';"
    ┌────────────────┬──────────────────────┬─────────┬───┬─────────┬─────────┐
    │  column_name   │     column_type      │  null   │ … │ default │  extra  │
    │    varchar     │       varchar        │ varchar │   │ varchar │ varchar │
    ├────────────────┼──────────────────────┼─────────┼───┼─────────┼─────────┤
    │ timestamp      │ UINTEGER             │ YES     │ … │         │         │
    │ latitude       │ FLOAT                │ YES     │ … │         │         │
    │ longitude      │ FLOAT                │ YES     │ … │         │         │
    │ altitude       │ INTEGER              │ YES     │ … │         │         │
    │ ground_speed   │ SMALLINT             │ YES     │ … │         │         │
    │ vertical_speed │ SMALLINT             │ YES     │ … │         │         │
    │ track          │ SMALLINT             │ YES     │ … │         │         │
    │ squawk         │ USMALLINT            │ YES     │ … │         │         │
    │ ems            │ STRUCT("timestamp"…  │ YES     │ … │         │         │
    ├────────────────┴──────────────────────┴─────────┴───┴─────────┴─────────┤
    │ 9 rows                                              6 columns (5 shown) │
    └─────────────────────────────────────────────────────────────────────────┘
    
    $ duckdb -c "describe select unnest(ems) from 'playback.parquet';"
    ┌──────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
    │ column_name  │ column_type │  null   │   key   │ default │  extra  │
    │   varchar    │   varchar   │ varchar │ varchar │ varchar │ varchar │
    ├──────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
    │ timestamp    │ UINTEGER    │ YES     │         │         │         │
    │ ias          │ SMALLINT    │ YES     │         │         │         │
    │ tas          │ SMALLINT    │ YES     │         │         │         │
    │ mach         │ SMALLINT    │ YES     │         │         │         │
    │ mcp          │ INTEGER     │ YES     │         │         │         │
    │ fms          │ INTEGER     │ YES     │         │         │         │
    │ autopilot    │ TINYINT     │ YES     │         │         │         │
    │ oat          │ TINYINT     │ YES     │         │         │         │
    │ track        │ FLOAT       │ YES     │         │         │         │
    │ roll         │ FLOAT       │ YES     │         │         │         │
    │ qnh          │ USMALLINT   │ YES     │         │         │         │
    │ wind_dir     │ SMALLINT    │ YES     │         │         │         │
    │ wind_speed   │ SMALLINT    │ YES     │         │         │         │
    │ precision    │ UTINYINT    │ YES     │         │         │         │
    │ altitude_gps │ INTEGER     │ YES     │         │         │         │
    │ emergency    │ UTINYINT    │ YES     │         │         │         │
    │ tcas_acas    │ UTINYINT    │ YES     │         │         │         │
    │ heading      │ USMALLINT   │ YES     │         │         │         │
    ├──────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
    │ 18 rows                                                  6 columns │
    └────────────────────────────────────────────────────────────────────┘

    $ duckdb -c "copy (select value from parquet_kv_metadata('playback.parquet') where key='_flight') to '/dev/stdout' (format json)" | jq -r '.value | gsub("\\\\x22"; "\"") | fromjson'
    {
        "flight_id": 47716903,
        "callsign": "MAS370",
        "flight_number": "MH370",
        "status_type": "departure",
        "status_text": null,
        "status_diverted": null,
        "status_time": null,
        "model_code": "B772",
        "icao24": 7667855,
        "registration": "9M-MRO",
        "owner": null,
        "airline": null,
        "origin": "WMKK",
        "destination": "ZBAA",
        "median_delay": null,
        "median_time": null
    }
    ```

TUI:

```
fr24 tui
```

Build and hotload documentation:

```sh
mkdocs serve
```

# Directories

Check the location of the config and cache directories with:
```sh
fr24 dirs
```
Here are possible outputs:

| OS      | Config File                                | Cache Directory                  |
| ------- | ------------------------------------------ | -------------------------------- |
| Linux   | `$HOME/.config/fr24/fr24.conf`             | `$HOME/.cache/fr24`              |
| macOS   | `$HOME/Library/Preferences/fr24.conf`      | `$HOME/Library/Caches/fr24`      |
| Windows | `%LOCALAPPDATA%\Acme\fr24\Cache\fr24.conf` | `%LOCALAPPDATA%\Acme\fr24\Cache` |