from __future__ import annotations

import asyncio
import secrets
import struct
import uuid
from pathlib import Path
from typing import Any

import httpx
from google.protobuf.json_format import MessageToDict

import pandas as pd

from .proto.request_pb2 import LiveFeedRequest, LiveFeedResponse
from .types.fr24 import Authentication

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) "
    "Gecko/20100101 Firefox/116.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "fr24-device-id": "web-00000000000000000000000000000000",
    "x-envoy-retry-grpc-on": "unavailable",
    "Content-Type": "application/grpc-web+proto",
    "X-User-Agent": "grpc-web-javascript/0.1",
    "X-Grpc-Web": "1",
    "Origin": "https://www.flightradar24.com",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.flightradar24.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
}


world_zones = [
    (90, 70, -180, 180),
    (70, 50, -180, -20),
    (70, 50, -20, 0),
    (70, 50, 0, 20),
    (70, 50, 20, 40),
    (70, 50, 40, 180),
    (50, 30, -180, -120),
    (50, 40, -120, -110),
    (50, 40, -110, -100),
    (40, 30, -120, -110),
    (40, 30, -110, -100),
    (50, 40, -100, -90),
    (50, 40, -90, -80),
    (40, 30, -100, -90),
    (40, 30, -90, -80),
    (50, 30, -80, -60),
    (50, 30, -60, -40),
    (50, 30, -40, -20),
    (50, 30, -20, 0),
    (50, 40, 0, 10),
    (50, 40, 10, 20),
    (40, 30, 0, 10),
    (40, 30, 10, 20),
    (50, 30, 20, 40),
    (50, 30, 40, 60),
    (50, 30, 60, 180),
    (30, 10, -180, -100),
    (30, 10, -100, -80),
    (30, 10, -80, 100),
    (30, 10, 100, 180),
    (10, -10, -180, 180),
    (-10, -30, -180, 180),
    (-30, -90, -180, 180),
]


def create_request(
    north: float = 50,
    south: float = 40,
    west: float = 0,
    east: float = 10,
    stats: bool = False,
    limit: int = 1500,
    maxage: int = 14400,
    auth: None | Authentication = None,
    **kwargs: Any,
) -> httpx.Request:
    request = LiveFeedRequest(
        bounds=LiveFeedRequest.Bounds(
            north=north, south=south, west=west, east=east
        ),
        settings=LiveFeedRequest.Settings(
            sources_list=range(10),  # type: ignore
            services_list=range(12),  # type: ignore
            traffic_type=LiveFeedRequest.Settings.ALL,
        ),
        field_mask=LiveFeedRequest.FieldMask(
            field_name=[
                "flight",
                "reg",
                "route",
                "type",
                "schedule",
            ]
            # auth required: squawk, vspeed, airspace
        ),
        stats=stats,
        limit=limit,
        maxage=maxage,
        **kwargs,
    )
    request_s = request.SerializeToString()
    post_data = b"\x00" + struct.pack("!I", len(request_s)) + request_s

    headers = DEFAULT_HEADERS.copy()
    headers["fr24-device-id"] = f"web-{secrets.token_urlsafe(32)}"
    if auth is not None and auth["userData"]["accessToken"] is not None:
        headers["authorization"] = f"Bearer {auth['userData']['accessToken']}"

    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed",
        headers=headers,
        content=post_data,
    )


async def post_request(
    client: httpx.AsyncClient, request: httpx.Request
) -> LiveFeedResponse:
    response = await client.send(request)
    data = response.content
    assert len(data) and data[0] == 0
    data_len = int.from_bytes(data[1:5], byteorder="big")
    lfr = LiveFeedResponse()
    lfr.ParseFromString(data[5 : 5 + data_len])
    return lfr


async def world_data(
    client: httpx.AsyncClient, auth: None | Authentication = None
) -> pd.DataFrame:
    results = await asyncio.gather(
        *[
            post_request(client, create_request(*bounds, auth=auth))
            for bounds in world_zones
        ]
    )

    return pd.concat(
        pd.json_normalize(
            MessageToDict(
                data,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                use_integers_for_enums=False,
            )["flights_list"]
        )
        for data in results
    )


def snapshot() -> None:
    async def export_parquet(filename: Path) -> None:
        async with httpx.AsyncClient() as client:
            df = await world_data(client)
            df.to_parquet(filename)

    filename = Path(str(uuid.uuid4())).with_suffix(".parquet")

    asyncio.run(export_parquet(filename))
    print(f"{filename.name} written")
