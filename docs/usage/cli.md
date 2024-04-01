# CLI
- List all commands and show help:

    === "Shell"

        ```
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
        │ auth   Commands for authentication                                           │
        │ dirs   Shows relevant directories                                            │
        │ feed   Fetches current livefeed / playback of live feed at a given time      │
        │ tui    Starts the TUI                                                        │
        ╰──────────────────────────────────────────────────────────────────────────────╯
        ```

- Dump the current (or playback of) live feed in a tidy parquet file:

    === "Shell"

        ```
        fr24 feed
        fr24 feed --timestamp 1702839380
        fr24 feed --time 2023-12-17T18:56:00
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
        │ heading        │ USMALLINT   │ YES     │         │         │         │
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