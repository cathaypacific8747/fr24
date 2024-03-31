import pytest
from fr24.core import FR24


@pytest.mark.asyncio
async def test_playback_simple() -> None:
    async with FR24() as fr24:
        pb = fr24.playback(flight_id=0x2D81A27)
        response = await pb.api.fetch()
        assert response["result"]["response"]["data"] is not None

        pb.data.add_api_response(response)
        assert pb.data.table is not None
        assert pb.data.table.num_rows == 62
        assert pb.data.table.num_columns == 9
        assert pb.data.df is not None
        assert pb.data.df.shape[0] == pb.data.table.num_rows
        assert pb.data.df.shape[1] == pb.data.table.num_columns


@pytest.mark.asyncio
async def test_flight_list_file_ops() -> None:
    """
    check that saving and reopening in a new instance yields the same rows
    make sure flight metadata is preserved and consistent.
    """
    async with FR24() as fr24:
        pb = fr24.playback(flight_id=0x2D81A27)

        # make directories and delete files if it exists
        pb.data.fp.parent.mkdir(parents=True, exist_ok=True)
        pb.data.fp.unlink(missing_ok=True)
        pb.data.add_api_response(await pb.api.fetch())

        assert pb.data.metadata is not None
        callsign = pb.data.metadata.get("callsign")

        assert pb.data.table is not None

        pb.data.save_parquet()
        assert pb.data.fp.stem == "2d81a27"
        assert pb.data.fp.exists()

        pb_local = fr24.playback(flight_id=0x2D81A27)
        pb_local.data.add_parquet()

        assert pb_local.data.table is not None
        assert pb_local.data.table.equals(pb.data.table)

        assert pb_local.data.metadata is not None
        callsign_local = pb_local.data.metadata.get("callsign")
        assert callsign_local == callsign
