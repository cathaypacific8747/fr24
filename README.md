# fr24

Download and parse data from flightradar24.com (gRPC and JSON).

## Installation

Clone the repository and run in the directory:

```sh
pip install .
```

For a development version, you may want to use Poetry:

```sh
poetry install
poetry shell
```

Once installed, a few endpoints are available (use `--help` for more information):

- Dump the current state vectors in a tidy parquet file:

  ```sh
  fr24 feed live
  fr24 feed playback --timestamp 1702839380
  fr24 feed playback --time 2023-12-17T18:56:00
  ```

- TUI:

  ```sh
  fr24 tui
  ```

- You may want to be authenticated to access more history: set the environment variables `fr24_username` and `fr24_password`, then check that you are properly authenticated with the following:

  ```sh
  fr24 auth show
  ```

- You may also create a configuration file in the config directory: you may find its location with:

  ```sh
  fr24 dirs
  ```

  On Linux, copy the content of `fr24.example.conf` to `$HOME/.config/fr24/fr24.conf`.

## Usage

Most code is developed in asynchronous mode: if you are not familiar with that programming style, wrap your code in an `async` function called `async_main`, and

- run `asyncio.run(main())` in a Python script;
- run `await main()` in a Jupyter notebook.

You can find usage examples in the `scripts/` folder.

### Caching

To avoid repeated requests, a [simple file-based cache](src/fr24/core.py) saves parquet files under the cache directory (`$HOME/.cache/fr24` on Linux).

## License

> [!IMPORTANT]  
> This code has been developed for educational purposes ONLY. Do not abuse it.

```json
{
  "copyright": "Copyright (c) 2014-2023 Flightradar24 AB. All rights reserved.",
  "legalNotice": "The contents of this file and all derived data are the property of Flightradar24 AB for use exclusively by its products and applications. Using, modifying or redistributing the data without the prior written permission of Flightradar24 AB is not allowed and may result in prosecutions."
}
```

## Notes

https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md

Generate stubs for pyarrow

```bash
stubgen -p pyarrow -o $PATH_TO_SITE_PACKAGES
```
