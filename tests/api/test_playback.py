import pytest
from pydantic import ConfigDict, TypeAdapter

from fr24 import FR24, Cache

FLIGHT_ID = 0x2D81A27


@pytest.mark.anyio
async def test_playback_simple(fr24: FR24) -> None:
    result = await fr24.playback.fetch(flight_id=FLIGHT_ID)
    assert result.to_dict()["result"]["response"]["data"] is not None

    df = result.to_polars()
    assert df.height == 62
    assert df.width == 9

    from fr24.types.playback import Playback

    class Playback_(Playback):
        __pydantic_config__ = ConfigDict(extra="forbid")  # type: ignore

    ta = TypeAdapter(Playback_)
    ta.validate_python(result.to_dict(), strict=True)


@pytest.mark.anyio
async def test_playback_file_ops(fr24: FR24, cache: Cache) -> None:
    """
    check that saving and reopening in a new instance yields the same rows
    """

    result = await fr24.playback.fetch(flight_id=FLIGHT_ID)

    fp = cache.path / "playback" / f"{format(FLIGHT_ID, 'x').lower()}.parquet"
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.unlink(missing_ok=True)
    result.write_table(fp)
    assert fp.exists()

    df_local = cache.playback.scan_table(FLIGHT_ID).collect()
    assert df_local.equals(result.to_polars())

    # NOTE: making sure that flight metadata is preserved and consistent
    # has been removed.
    # meta_local = datac_local.metadata
    # assert meta_local is not None
    # assert meta_local.get("callsign") == meta.get("callsign")

    fp.unlink()
