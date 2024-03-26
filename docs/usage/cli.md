# Quick Start
- List all commands and show help:

    ```
    fr24 --help
    ```

- Dumping the current state vectors in a tidy parquet file:

    ```
    fr24 feed live
    fr24 feed playback --timestamp 1702839380
    fr24 feed playback --time 2023-12-17T18:56:00
    ```

- TUI

    ```
    fr24 tui
    ```

# Authentication
You may want to be authenticated to access more history: set the environment variables `fr24_username` and `fr24_password`, then check that you are properly authenticated:

```sh
fr24 auth show
```

You may also create a configuration file in the [config directory](#directories): an example of it can be found at [`fr24.example.conf`](https://github.com/cathaypacific8747/fr24/blob/master/fr24.example.conf).

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