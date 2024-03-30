# %%
# ruff: noqa: F704, F811, E402
from fr24.core import FR24


async def my_full_list() -> None:
    async with FR24() as fr24:
        fl = fr24.flight_list(reg="B-KJA")
        fl.data.add_api_response(await fl.api.fetch())
        print(fl.data.df)
        fl.data.save_parquet()


await my_full_list()  # type: ignore
# %%
