import pytest

from fr24 import FR24Cache
from fr24.service import NearestFlightsResult


@pytest.mark.anyio
async def test_nearest_flights_simple(
    nearest_flights_result: NearestFlightsResult,
) -> None:
    num_flights = len(nearest_flights_result.to_proto().flights_list)
    assert len(nearest_flights_result.to_proto().flights_list) > 2

    df = nearest_flights_result.to_polars()
    assert df.height == num_flights
    assert df.width == 19


@pytest.mark.anyio
async def test_nearest_flights_file_ops(
    nearest_flights_result: NearestFlightsResult, cache: FR24Cache
) -> None:
    lon = nearest_flights_result.request.lon
    lat = nearest_flights_result.request.lat
    timestamp = nearest_flights_result.timestamp
    ident = f"{int(lon * 1e6)}_{int(lat * 1e6)}_{timestamp}"
    fp = cache.path / "nearest_flights" / f"{ident}.parquet"
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.unlink(missing_ok=True)

    nearest_flights_result.write_table(cache)
    assert fp.exists()

    df_local = cache.nearest_flights.scan_table(ident).collect()
    assert df_local.equals(nearest_flights_result.to_polars())

    fp.unlink()
