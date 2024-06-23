# CLI
- List all commands and show help:

    === "Shell"

        ```
        fr24 --help
        ```
    
    === "Output"
        
        ```
        Usage: fr24 [OPTIONS] COMMAND [ARGS]...                                                
                                                                                                
        ╭─ Options ────────────────────────────────────────────────────────────────────────────╮
        │ --install-completion          Install completion for the current shell.              │
        │ --show-completion             Show completion for the current shell, to copy it or   │
        │                               customize the installation.                            │
        │ --help                        Show this message and exit.                            │
        ╰──────────────────────────────────────────────────────────────────────────────────────╯
        ╭─ Commands ───────────────────────────────────────────────────────────────────────────╮
        │ auth          Commands for authentication                                            │
        │ dirs          Shows relevant directories                                             │
        │ feed          Fetches current livefeed / playback of live feed at a given time       │
        │ flight-list   Fetches flight list for the given registration or flight number        │
        │ playback      Fetches historical track playback data for the given flight            │
        │ tui           Starts the TUI                                                         │
        ╰──────────────────────────────────────────────────────────────────────────────────────╯
        ```

- Dump the current (or playback of) live feed in a tidy parquet file:

    === "Shell"

        ```
        fr24 feed
        fr24 feed --timestamp 1702839380
        fr24 feed --timestamp 2023-12-17T18:56:00
        fr24 feed --help
        ```

    === "Output"
    
        ```command
        $ fr24 feed
        Success: Saved 12345 rows (533568 bytes) to /home/user/.cache/fr24/feed/1234567890.parquet.
        
        $ duckdb -c "describe select * from '/home/user/.cache/fr24/feed/1234567890.parquet';"
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
        ├────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
        │ 16 rows                                                    6 columns │
        └──────────────────────────────────────────────────────────────────────┘
        ```

- Dump the 

    === "Shell"

        ```
        fr24 flight-list --reg B-HPB
        fr24 flight-list --flight CX488
        fr24 flight-list --help
        ```

    === "Output"
    
        ```command
        $ fr24 flight-list --reg B-HPB
        Success: Saved 10 rows (1290 bytes) to /home/user/.cache/fr24/flight_list/reg/B-HPB.parquet.
        
        $ duckdb -c "describe select * from '/home/user/.cache/fr24/flight_list/reg/B-HPB.parquet';"

        ```
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

- Dump the historical track playback data for the given flight

    === "Shell"

        ```
        fr24 playback 2d81a27
        fr24 playback --help
        ```

    === "Output"
    
        ```command
        $ fr24 playback 2d81a27
        Success: Saved 62 rows (4162 bytes) to /home/user/.cache/fr24/playback/2d81a27.parquet.
        
        $ duckdb -c "describe select * from '/home/user/.cache/fr24/playback/2d81a27.parquet'"
        ┌────────────────┬───────────────────────────────┬─────────┬─────────┬─────────┬─────────┐
        │  column_name   │          column_type          │  null   │   key   │ default │  extra  │
        │    varchar     │            varchar            │ varchar │ varchar │ varchar │ varchar │
        ├────────────────┼───────────────────────────────┼─────────┼─────────┼─────────┼─────────┤
        │ timestamp      │ UINTEGER                      │ YES     │         │         │         │
        │ latitude       │ FLOAT                         │ YES     │         │         │         │
        │ longitude      │ FLOAT                         │ YES     │         │         │         │
        │ altitude       │ INTEGER                       │ YES     │         │         │         │
        │ ground_speed   │ SMALLINT                      │ YES     │         │         │         │
        │ vertical_speed │ SMALLINT                      │ YES     │         │         │         │
        │ track          │ SMALLINT                      │ YES     │         │         │         │
        │ squawk         │ USMALLINT                     │ YES     │         │         │         │
        │ ems            │ STRUCT("timestamp" UINTEGER…  │ YES     │         │         │         │
        └────────────────┴───────────────────────────────┴─────────┴─────────┴─────────┴─────────┘
        ```

- TUI:

    ```
    fr24 tui
    ```

- Build and hotload documentation:

    ```sh
    mkdocs serve
    ```

    Navigate to localhost:8000.

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