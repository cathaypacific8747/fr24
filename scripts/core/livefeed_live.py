# %%
# ruff: noqa: F704, F811, E402
from fr24.core import FR24


async def my_feed() -> None:
    async with FR24() as fr24:
        lf = fr24.livefeed()
        print(lf.data.fp)
        lf.data.add_api_response(await lf.api.fetch())
        print(lf.data.df)
        lf.data.save_parquet()


await my_feed()  # type: ignore

# %%
