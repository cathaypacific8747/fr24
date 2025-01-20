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

However, the [FR24][fr24.FR24] class provides a convenient wrapper around them. It:

- Manages a shared HTTP client and authentication state
- Has three services:
    - [**Live Feed**][fr24.service.LiveFeedService]: snapshot of all aircraft state vectors
    - [**Flight List**][fr24.service.FlightListService]: all historical flights for a given aircraft registration or flight number
    - [**Playback**][fr24.service.PlaybackService]: historical trajectory for one flight.

!!! warn
    The following section is for `fr24<v0.2.0`, and will be updated.

Each service has its own async `.fetch()` method to retrieve raw data from the API. `.to_arrow()` can then be used to transform to an Apache Arrow table, and used to perform caching and downstream `pandas` operations.

Here is an example for using the [**Live Feed**][fr24.service.LiveFeedService] service:

### Initialisation

=== "example.py"

    ```py hl_lines="4"
    --8<-- "docs/usage/scripts/01_live_feed_live.py:script"
    ```

=== "`result`"
    
    ```py
    --8<-- "docs/usage/scripts/01_live_feed_live.py:result"
    ```

=== "`data` (truncated)"
    
    ```json
    --8<-- "docs/usage/scripts/01_live_feed_live.py:data"
    ```

=== "`datac.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_live_feed_live.py:df"
    ```

When `FR24()` is first initialised, it creates an unauthenticated [HTTPX client](https://www.python-httpx.org/async/) under the hood.

!!! question "How to authenticate?"

    ```py
    --8<-- "docs/usage/scripts/00_introduction.py:login"
    ```

    See [authentication](./authentication.md) for more details.

!!! question "How to pass in my own HTTPX client?"
    
    To share clients across code, pass it into the [fr24.FR24][] constructor.

    ```py
    --8<-- "docs/usage/scripts/00_introduction.py:client-sharing"
    ```

The `async with` statement ensures that it is properly authenticated by calling the login endpoint (if necessary).

### Fetching from API

=== "Jupyter cell"

    ```py hl_lines="5"
    --8<-- "docs/usage/scripts/01_live_feed_live.py:script"
    ```

=== "`response`"
    
    ```py
    --8<-- "docs/usage/scripts/01_live_feed_live.py:response"
    ```

=== "`datac.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_live_feed_live.py:df"
    ```

`fr24.live_feed` returns a [LiveFeedService][fr24.service.LiveFeedService], with the following methods:

| Method                                                                                        | Return type                    |
| --------------------------------------------------------------------------------------------- | ------------------------------ |
| `.fetch` - [asynchronously query the the API for fresh data][fr24.service.LiveFeedService.fetch] | [fr24.service.LiveFeedAPIResp][]  |
| `.load` - [load a previously cached snapshot from the disk][fr24.service.LiveFeedService.load]   | [fr24.service.LiveFeedArrow][]    |

You can retrieve:

- the [context related to the request][fr24.types.core.LiveFeedContext] with `response.ctx`;
- the [raw JSON response][fr24.types.cache.LiveFeedRecord] as a list of typed dictionaries with `response.data`.

### Transformation to Arrow

In practice, you could directly pipe `response.data` into `pd.DataFrame.from_records()`, but pandas
uses 64-bit integers by default and can be storage-inefficient.

=== "Jupyter cell"

    ```py hl_lines="6"
    --8<-- "docs/usage/scripts/01_live_feed_live.py:script"
    ```

=== "`response`"
    
    ```py
    --8<-- "docs/usage/scripts/01_live_feed_live.py:response"
    ```

=== "`datac.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_live_feed_live.py:df"
    ```

Instead, you can call `.to_arrow()`, which creates a new
[strongly typed][fr24.types.cache.live_feed_schema] Apache Arrow table from it.

[Arrow](https://arrow.apache.org/docs/index.html) is a columnar data storage format
with [excellent interoperability](https://arrow.apache.org/docs/python/pandas.html)
with `pd.DataFrame`. You can retrieve:

- the [context related to the request][fr24.types.core.LiveFeedContext] with `datac.ctx`;
- the underlying [Arrow table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) with `datac.data`;
- get the pandas representation with `datac.df`.

### Saving to Disk

=== "Jupyter cell"

    ```py hl_lines="7"
    --8<-- "docs/usage/scripts/01_live_feed_live.py:script"
    ```

=== "`response`"
    
    ```py
    --8<-- "docs/usage/scripts/01_live_feed_live.py:response"
    ```

=== "`datac.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_live_feed_live.py:df"
    ```

`.save()` writes the table to the default cache directory[^1] using the [Parquet](https://parquet.apache.org/)
data format.

You can always check its exact location using `datac.fp`. In general, where it gets saved is as follows:

### Storage Location

- [Live feed][fr24.service.LiveFeedService]
    - `feed/{timestamp}.parquet`
- [Flight list][fr24.service.FlightListService]
    - `flight_list/reg/{reg.upper()}.parquet`, or
    - `flight_list/flight/{iata_flight_num.upper()}.parquet`
- [Playback][fr24.service.PlaybackService]
    - `playback/{fr24_hex_id.lower()}.parquet`

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
These directories are created automatically whenever `datac.save()` is called.

### Reading from disk

=== "Jupyter cell"

    ```py hl_lines="5"
    --8<-- "docs/usage/scripts/01_live_feed_live.py:script2"
    ```

=== "`datac.df`"
    
    ```
    --8<-- "docs/usage/scripts/01_live_feed_live.py:df"
    ```

To retrieve saved data, first pass in the unique identifier (timestamp in this case) to the `.load()`.

## Notes

Each service inherits from the [fr24.base.ServiceBase][] and have similar APIs demonstrated above.

See the [examples gallery](./examples.md) to learn more.

!!! tip
    
    Pyarrow unfortunately do not provide type hints. You can however, generate the stubs to your `site-packages` directory with:

    ```sh
    $ stubgen -p pyarrow -o $(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
    ```

Intersphinx for this project could be found [here](https://cathaypacific8747.github.io/fr24/objects.inv).

[^1]: You can check its location by [running `fr24 dirs` in the shell](./cli.md#directories).