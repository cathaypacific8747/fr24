# ruff: noqa
# fmt: off
# %%
# --8<-- [start:script]
import asyncio
from fr24.find import find

async def main():  # (1)!
    list_ = await find("Toulouse")  # (2)!
    print(list_)

if __name__ == "__main__":
    asyncio.run(main())  # (3)!
# --8<-- [end:script]
# %%
# --8<-- [start:jupyter]
from fr24.find import find

async def main(): # (1)!
    list_ = await find("Toulouse") # (2)!
    print(list_)

await main()
# --8<-- [end:jupyter]
# %%
# --8<-- [start:output]
{
    "results": [
        {
            "id": "TLS",
            "label": "Toulouse Blagnac Airport (TLS / LFBO)",
            "detail": {"lat": 43.628101, "lon": 1.367263, "size": 33922},
            "type": "airport",
            "match": "begins",
        },
        # ...
    ]
}
# --8<-- [end:output]
#%%
