# %%
# ruff: noqa: F704, F811, E402
import rich
from fr24.core import FR24


async def my_playback() -> None:
    async with FR24() as fr24:
        fl = fr24.playback(flight_id=0x2D81A27)
        fl.data.fp.unlink(missing_ok=True)
        fl.data.add_api_response(await fl.api.fetch())
        print(fl.data.df)
        fl.data.save_parquet()

        fl.data.clear()
        fl.data.add_parquet()
        rich.print(fl.data.metadata)


await my_playback()  # type: ignore

# %%
