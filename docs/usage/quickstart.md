## Async
Most code is developed using asynchronous programming, enabling parallel execution of multiple queries and achieve high performance.

Here is a quick example in case you are not familiar with this code style:

=== "Python Script"

    ```py
    --8<-- "docs/usage/scripts/00_introduction.py:script"
    ```
    
    1. Wrap your code in an `async` function
    2. `find()` is an asynchronous function - we need to `await` it
    3. `main()` returns a coroutine object which does not run immediately - we need to run it on the event loop

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/00_introduction.py:jupyter"
    ```

    1. Wrap your code in an `async` function
    2. `find()` is an asynchronous function - we need to `await` it

=== "Output"

    ```py
    --8<-- "docs/usage/scripts/00_introduction.py:output"
    ```

## The `FR24` Class

Most of the core code are developed in [many tiny functions](../api/functions.md) for flexibility.

However, the [FR24][fr24.core.FR24] class provides a convenient wrapper around them. It:

- Manages a shared HTTP client and authentication state
- Has three services:
    - [**Live Feed**][fr24.core.FR24.livefeed]: snapshot of all aircraft state vectors
    - [**Flight List**][fr24.core.FR24.flight_list]: all historical flights for a given aircraft registration or flight number
    - [**Playback**][fr24.core.FR24.playback]: historical trajectory for one flight.

Each service has its own `.api.fetch()` function to retrieve data from the API. The `.data.*` functions can then be used perform file-based operations, such as writing to disk and downstream `pandas` operations.

Here is an example for using the [**Live Feed**][fr24.core.FR24.livefeed] service:

### Initialisation

=== "example.py"

    ```py hl_lines="4"
    --8<-- "docs/usage/scripts/01_livefeed_live.py:script"
    ```

=== "`response`"
    
    ```py
    --8<-- "docs/usage/scripts/01_livefeed_live.py:response"
    ```

=== "`lf.data.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_livefeed_live.py:df"
    ```

When `FR24()` is first initialised, it creates the [HTTP client](https://www.python-httpx.org/async/) under the hood.

The `async with` statement ensures that it is properly authenticated before any actions are performed (if [configured](./authentication.md)).

### Choosing the service

=== "Jupyter cell"

    ```py hl_lines="5"
    --8<-- "docs/usage/scripts/01_livefeed_live.py:script"
    ```

=== "`response`"
    
    ```py
    --8<-- "docs/usage/scripts/01_livefeed_live.py:response"
    ```

=== "`lf.data.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_livefeed_live.py:df"
    ```

Next, `fr24.livefeed()` creates a new [LiveFeedService][fr24.core.LiveFeedService], with the following member variables:

| Member  | Type                                | Description                             |
| ------- | ----------------------------------- | --------------------------------------- |
| `.api`  | [fr24.core.LiveFeedAPI][]           | interacts with the API                  |
| `.data` | [fr24.core.LiveFeedArrow][]         | store data and read/write files         |
| `.ctx`  | [fr24.types.core.LiveFeedContext][] | holds essential context for the request |

### Fetching and transformation

=== "Jupyter cell"

    ```py hl_lines="6 8 9"
    --8<-- "docs/usage/scripts/01_livefeed_live.py:script"
    ```

=== "`response`"
    
    ```py
    --8<-- "docs/usage/scripts/01_livefeed_live.py:response"
    ```

=== "`lf.data.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_livefeed_live.py:df"
    ```

Here, `.api.fetch()` calls the API and returns the raw response as Python dictionaries.

In practice, you could directly pipe this into `pd.DataFrame.from_records()`, but pandas
uses 64-bit integers by default and can be storage-inefficient.

Instead, you can call `.data.add_api_response()`, which creates a new
[strongly typed][fr24.types.cache.livefeed_schema] Apache Arrow table from it.

[Arrow](https://arrow.apache.org/docs/index.html) is a columnar data storage format
with [excellent interoperability](https://arrow.apache.org/docs/python/pandas.html)
with `pd.DataFrame`. You can retrieve the underlying Arrow table with `.data.table`, or
retrieve its pandas equivalent with `.data.df`.

### Saving to Disk

Finally, you can save `.data.table` to the [Parquet](https://parquet.apache.org/)
data format.

=== "Jupyter cell"

    ```py hl_lines="10 11"
    --8<-- "docs/usage/scripts/01_livefeed_live.py:script"
    ```

=== "`response`"
    
    ```py
    --8<-- "docs/usage/scripts/01_livefeed_live.py:response"
    ```

=== "`lf.data.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_livefeed_live.py:df"
    ```

By default, `.save_parquet()` saves it under the default cache directory[^1].

You can always check its exact location using `.data.fp`. In general, where it gets saved is as follows:

### Storage Location

- [Flight list][fr24.core.FR24.flight_list]
    - `flight_list/reg/{reg.upper()}.parquet`, or
    - `flight_list/flight/{iata_flight_num.upper()}.parquet`
- [Playback][fr24.core.FR24.playback]
    - `playback/{fr24_hex_id.lower()}.parquet`
- [Live feed][fr24.core.FR24.livefeed]
    - `feed/{timestamp}.parquet`

It should resemble the following on Linux:
```
$ tree $HOME/.cache/fr24/feed
/home/user/.cache/fr24
├── feed
│   ├── 1711911907.parquet
├── flight_list
│   ├── flight
│   │   └── CX8747.parquet
│   └── reg
│       └── B-HUJ.parquet
└── playback
    └── 2d81a27.parquet
```
These directories are created automatically whenever `.save_parquet()` is called.

### Reading from disk

=== "Jupyter cell"

    ```py hl_lines="5 6"
    --8<-- "docs/usage/scripts/01_livefeed_live.py:script2"
    ```

=== "`lf.data.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_livefeed_live.py:df"
    ```

To retrieve saved data, first pass in the unique identifier (timestamp in this case) to the service constructor.

Then, instead of calling `.data.add_api_response()`, use `.add_parquet()`.

## Notes

Each service inherits from the [fr24.base.ServiceBase][] and have similar APIs demonstrated above.

See the [examples gallery](./examples.md) to learn more.

!!! tip
    Pyarrow unfortunately do not provide type hints. You can however, generate the stubs with:
    ```sh
    stubgen -p pyarrow -o $PATH_TO_SITE_PACKAGES
    ```

Intersphinx for this project could be found [here](https://cathaypacific8747.github.io/fr24/objects.inv).

[^1]: You can check its location by [running `fr24 dirs` in the shell](./cli.md#directories).