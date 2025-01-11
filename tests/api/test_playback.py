import pytest
from pydantic import ConfigDict, TypeAdapter

from fr24.core import FR24
from fr24.types.playback import Playback

FLIGHT_ID = 0x2D81A27


@pytest.mark.anyio
async def test_playback_simple(fr24: FR24) -> None:
    response = await fr24.playback.fetch(flight_id=FLIGHT_ID)
    assert response.data["result"]["response"]["data"] is not None

    datac = response.to_arrow()
    assert datac.data.num_rows == 62
    assert datac.data.num_columns == 9

    df = datac.df
    assert df.shape[0] == datac.data.num_rows
    assert df.shape[1] == datac.data.num_columns

    class Playback_(Playback):
        __pydantic_config__ = ConfigDict(extra="forbid")  # type: ignore

    ta = TypeAdapter(Playback_)
    ta.validate_python(response.data, strict=True)


@pytest.mark.anyio
async def test_playback_file_ops(fr24: FR24) -> None:
    """
    check that saving and reopening in a new instance yields the same rows
    make sure flight metadata is preserved and consistent.
    """
    response = await fr24.playback.fetch(flight_id=FLIGHT_ID)

    datac = response.to_arrow()
    meta = datac.metadata
    assert meta is not None

    fp = (
        fr24.base_dir / "playback" / f"{format(FLIGHT_ID, 'x').lower()}.parquet"
    )
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.unlink(missing_ok=True)
    datac.save()
    assert fp.exists()

    datac_local = fr24.playback.load(flight_id=FLIGHT_ID)
    assert datac_local.data.num_rows == datac.data.num_rows
    assert datac_local.data.equals(datac.data)

    meta_local = datac_local.metadata
    assert meta_local is not None
    assert meta_local.get("callsign") == meta.get("callsign")

    fp.unlink()
