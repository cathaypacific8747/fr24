import pytest
from pydantic import ConfigDict, TypeAdapter

from fr24 import FR24
from fr24.types.playback import Playback

FLIGHT_ID = 0x2D81A27


@pytest.mark.anyio
async def test_playback_simple(fr24: FR24) -> None:
    result = await fr24.playback.fetch(flight_id=FLIGHT_ID)
    assert result.to_dict()["result"]["response"]["data"] is not None

    df = result.to_polars()
    assert df.height == 62
    assert df.width == 9

    class Playback_(Playback):
        __pydantic_config__ = ConfigDict(extra="forbid")  # type: ignore

    ta = TypeAdapter(Playback_)
    ta.validate_python(result.to_dict(), strict=True)


@pytest.mark.anyio
async def test_playback_file_ops(fr24: FR24) -> None:
    """
    check that saving and reopening in a new instance yields the same rows
    """

    result = await fr24.playback.fetch(flight_id=FLIGHT_ID)

    fp = (
        fr24.base_dir / "playback" / f"{format(FLIGHT_ID, 'x').lower()}.parquet"
    )
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.unlink(missing_ok=True)
    result.save(fp)
    assert fp.exists()

    df = result.to_polars()
    datac_local = fr24.playback.load(flight_id=FLIGHT_ID)  # FIXME
    assert datac_local.data.num_rows == df.height
    assert datac_local.data.equals(df)

    # NOTE: making sure that flight metadata is preserved and consistent
    # has been removed.
    # meta_local = datac_local.metadata
    # assert meta_local is not None
    # assert meta_local.get("callsign") == meta.get("callsign")

    fp.unlink()
