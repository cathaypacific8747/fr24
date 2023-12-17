# fr24

Download and parse data from flightradar24.com (gRPC and JSON).

## Installation

Clone the repository and run in the directory:

```sh
pip install .
```

For a development version, you may want to the poetry virtual environment:

```sh
poetry install
poetry shell
```

Few endpoints are available:

- Dump the current state vectors in a tidy parquet file:

  ```sh
  fr24_snapshot
  ```

- You may want to be authenticated for access to more history. Use environment variables `fr24_username` and `fr24_password`, then check that you are properly authenticated with the following:

  ```sh
  fr24_login
  ```

  You can also create a configuration file in the appropriate directory. For Linux, copy the content of `fr24.example.conf` to `$HOME/.config/fr24/fr24.conf`. For other operating systems, you will find the proper directory with the following code:

  ```sh
  python3 -c "from appdirs import user_config_dir; print(user_config_dir('fr24'))"
  ```

## Usage

Most code is developed in asynchronous mode: if you are not familiar with that programming style, wrap your code in an `async` function called `async_main`, and
  - run `asyncio.run(main())` in a Python script;
  - run `await main()` in a Jupyter notebook.

You can find usage examples in the `scripts/` folder.

### Caching

To avoid repeated requests, a [simple file-based cache](src/fr24/core.py) is under development. It saves parquet files under `$HOME/.cache/fr24` on Linux. You can find the cache directory on other operating systems with:

```sh
python3 -c "from appdirs import user_cache_dir; print(user_cache_dir('fr24'))"
```

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