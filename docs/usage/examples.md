You can find even more usage examples under [`tests/`](https://github.com/cathaypacific8747/fr24/tree/master/tests).

[Skip to lower level functions](#functional-style)

## `FR24` class

### Flight list
*API reference: [fr24.core.FlightListService][], [fr24.core.FlightListService.fetch][], [fr24.core.FlightListService.fetch_all][]*

#### Single page
=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/10_flight_list.py:script0"
    ```

=== "`data.df`"
    
    ```
    --8<-- "docs/usage/scripts/10_flight_list.py:df0"
    ```

#### Paginate all pages
Queries for next page as long as user doesn't enter `x`, or if there are no pages left.
In each iteration, rows are upserted and saved to the [cache](../usage/cli.md#directories).

Note that pagination cannot be run in parallel: fetching page N requires information from page N-1.

=== "Jupyter cell"

    ```py hl_lines="5 8"
    --8<-- "docs/usage/scripts/10_flight_list.py:script1"
    ```

    1. First attempt to load existing table from the [cache](../usage/cli.md#directories), otherwise it creates an empty in-memory arrow table for us to concat to.
    2. [Upserts the data][fr24.core.FlightListArrow.concat], replacing older records with new ones.

=== "`data.df`"
    
    ```
    --8<-- "docs/usage/scripts/10_flight_list.py:df1"
    ```

### Playback
*API reference: [fr24.core.PlaybackService][], [fr24.core.PlaybackService.fetch][]*

#### Miracle on the Hudson
Downloads the flight trajectory for [UA1549](https://en.wikipedia.org/wiki/US_Airways_Flight_1549)

=== "Jupyter cell"

    ```py hl_lines="6"
    --8<-- "docs/usage/scripts/11_playback.py:script0"
    ```

    1. From https://www.flightradar24.com/data/pinned/ua1549-2fb3041#2fb3041.

=== "`data.df`"
    
    ```
    --8<-- "docs/usage/scripts/11_playback.py:df0"
    ```

=== "`data.metadata`"
    
    ```py
    --8<-- "docs/usage/scripts/11_playback.py:metadata0"
    ```

#### File operations
Saves trajectory data to disk, reads the track and metadata from it.

=== "Jupyter cell"

    ```py hl_lines="8 10"
    --8<-- "docs/usage/scripts/11_playback.py:script1"
    ```
    
    1. Saves the parquet to the [cache](../usage/cli.md#directories).
    2. Load the parquet from the [cache](../usage/cli.md#directories).

=== "`data_local.df`"
    
    ```
    --8<-- "docs/usage/scripts/11_playback.py:df0"
    ```

=== "`data_local.metadata`"
    
    ```py
    --8<-- "docs/usage/scripts/11_playback.py:metadata0"
    ```
<!-- ### Live Feed
*API reference: [fr24.core.FR24.livefeed][], [fr24.core.LiveFeedAPI.fetch][]*

#### Live
This example is covered in detail in the [quickstart](./quickstart.md).

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/12_livefeed.py:script"
    ```

=== "`response`"
    
    ```py
    --8<-- "docs/usage/scripts/12_livefeed.py:response"
    ```

=== "`lf.data.df`"
    
    ```
    --8<-- "docs/usage/scripts/12_livefeed.py:df"
    ```

#### Playback
Fetches the live feed three days ago.

=== "Jupyter cell"

    ```py hl_lines="6"
    --8<-- "docs/usage/scripts/12_livefeed.py:script2"
    ```

    1. Subtract current UTC by 3 days.

=== "`lf.data.df`"
    
    ```
    --8<-- "docs/usage/scripts/12_livefeed.py:df2"
    ``` -->

## Functional Style
### Flight list
*API Reference: [fr24.history.flight_list][], [fr24.history.flight_list_df][]*

=== "Jupyter cell"

    ```py hl_lines="16"
    --8<-- "docs/usage/scripts/20_flight_list.py:script0"
    ```

    1. Replace it with the current time.

=== "`df`"
    
    ```
    --8<-- "docs/usage/scripts/20_flight_list.py:df0"
    ```

### Playback
*API Reference: [fr24.history.playback][], [fr24.history.playback_df][]*

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/21_playback.py:script0"
    ```

=== "`df`"
    
    ```
    --8<-- "docs/usage/scripts/21_playback.py:df0"
    ```

### Airport Arrivals

*API Reference: [fr24.history.airport_list][]*

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/22_arrivals.py:script0"
    ```

=== "`df`"
    
    ```
    --8<-- "docs/usage/scripts/22_arrivals.py:df0"
    ```

### Airport Search
*API Reference: [fr24.find][]*

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/23_find.py:script0"
    ```

=== "`df`"
    
    ```
    --8<-- "docs/usage/scripts/23_find.py:df0"
    ```

### Live feed
*API Reference: [fr24.livefeed][]*

Demonstrates custom bounding boxes.

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/24_livefeed.py:script0"
    ```

=== "Protobuf Output"
    
    ```proto
    --8<-- "docs/usage/scripts/24_livefeed.py:output0"
    ```

In JSON format:

=== "Jupyter cell"

    ```py
    --8<-- "docs/usage/scripts/24_livefeed.py:script1"
    ```

=== "Output"
    
    ```py
    --8<-- "docs/usage/scripts/24_livefeed.py:output1"
    ```
