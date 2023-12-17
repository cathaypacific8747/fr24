from __future__ import annotations

import asyncio
import secrets
import struct
from typing import Any

import httpx

from .common import DEFAULT_HEADERS_GRPC
from .proto.request_pb2 import (
    LiveFeedPlaybackRequest,
    LiveFeedPlaybackResponse,
    LiveFeedRequest,
    LiveFeedResponse,
)
from .types.cache import LiveFeedRecord
from .types.fr24 import Authentication

# N, S, W, E
lng_bounds = [
    -180,
    -117,
    -110,
    -100,
    -95,
    -90,
    -85,
    -82,
    -79,
    -75,
    -68,
    -30,
    -2,
    1,
    5,
    8,
    11,
    15,
    20,
    30,
    40,
    60,
    100,
    110,
    120,
    140,
    180,
]
world_zones = [
    (90, -90, lng_bounds[i], lng_bounds[i + 1])
    for i in range(len(lng_bounds) - 1)
]


def livefeed_message_create(
    north: float = 50,
    south: float = 40,
    west: float = 0,
    east: float = 10,
    stats: bool = False,
    limit: int = 1500,
    maxage: int = 14400,
    **kwargs: Any,
) -> LiveFeedRequest:
    return LiveFeedRequest(
        bounds=LiveFeedRequest.Bounds(
            north=north, south=south, west=west, east=east
        ),
        settings=LiveFeedRequest.Settings(
            sources_list=range(10),  # type: ignore
            services_list=range(12),  # type: ignore
            traffic_type=LiveFeedRequest.Settings.ALL,
            only_restricted=False,
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
        highlight_mode=False,
        stats=stats,
        limit=limit,
        maxage=maxage,
        restriction_mode=LiveFeedRequest.NOT_VISIBLE,
        **kwargs,
    )


def livefeed_playback_message_create(
    message: LiveFeedRequest,
    timestamp: int,
    prefetch: int,
    hfreq: int,
) -> LiveFeedPlaybackRequest:
    return LiveFeedPlaybackRequest(
        live_feed_request=message,
        timestamp=timestamp,
        prefetch=prefetch,
        hfreq=hfreq,
    )


def livefeed_request_create(
    message: LiveFeedRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    request_s = message.SerializeToString()
    post_data = b"\x00" + struct.pack("!I", len(request_s)) + request_s

    headers = DEFAULT_HEADERS_GRPC.copy()
    headers["fr24-device-id"] = f"web-{secrets.token_urlsafe(32)}"
    if auth is not None and auth["userData"]["accessToken"] is not None:
        headers["authorization"] = f"Bearer {auth['userData']['accessToken']}"

    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed",
        headers=headers,
        content=post_data,
    )


def livefeed_playback_request_create(
    message: LiveFeedPlaybackRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    request_s = message.SerializeToString()
    post_data = b"\x00" + struct.pack("!I", len(request_s)) + request_s

    headers = DEFAULT_HEADERS_GRPC.copy()
    headers["fr24-device-id"] = f"web-{secrets.token_urlsafe(32)}"
    if auth is not None and auth["userData"]["accessToken"] is not None:
        headers["authorization"] = f"Bearer {auth['userData']['accessToken']}"

    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/Playback",
        headers=headers,
        content=post_data,
    )


async def livefeed_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> bytes:
    response = await client.send(request)
    data = response.content
    assert len(data) and data[0] == 0
    data_len = int.from_bytes(data[1:5], byteorder="big")
    return data[5 : 5 + data_len]


def livefeed_response_parse(data: bytes) -> LiveFeedResponse:
    lfr = LiveFeedResponse()
    lfr.ParseFromString(data)
    return lfr


def livefeed_playback_response_parse(data: bytes) -> LiveFeedResponse:
    lfr = LiveFeedPlaybackResponse()
    lfr.ParseFromString(data)
    return lfr.live_feed_response


def livefeed_flightdata_dict(
    lfr: LiveFeedResponse.FlightData
) -> LiveFeedRecord:
    return {
        "flightid": lfr.flightid,
        "latitude": lfr.latitude,
        "longitude": lfr.longitude,
        "heading": lfr.heading,
        "altitude": lfr.altitude,
        "ground_speed": lfr.ground_speed,
        "timestamp": lfr.timestamp,
        "on_ground": lfr.on_ground,
        "callsign": lfr.callsign,
        "source": lfr.source,
        "registration": lfr.extra_info.reg,
        "origin": lfr.extra_info.route.from_,
        "destination": lfr.extra_info.route.to,
        "typecode": lfr.extra_info.type,
        "eta": lfr.extra_info.schedule.eta,
    }


async def livefeed_world_data(
    client: httpx.AsyncClient, auth: None | Authentication = None
) -> list[LiveFeedRecord]:
    results = await asyncio.gather(
        *[
            livefeed_post(
                client,
                livefeed_request_create(
                    livefeed_message_create(*bounds), auth=auth
                ),
            )
            for bounds in world_zones
        ]
    )
    return [
        livefeed_flightdata_dict(lfr)
        for r in results
        for lfr in livefeed_response_parse(r).flights_list
    ]


async def livefeed_playback_world_data(
    client: httpx.AsyncClient,
    timestamp: int,
    duration: int = 7,
    hfreq: int = 0,
    auth: None | Authentication = None,
) -> list[LiveFeedRecord]:
    results = await asyncio.gather(
        *[
            livefeed_post(
                client,
                livefeed_playback_request_create(
                    livefeed_playback_message_create(
                        livefeed_message_create(*bounds),
                        timestamp,
                        timestamp + duration,
                        hfreq,
                    ),
                    auth=auth,
                ),
            )
            for bounds in world_zones
        ]
    )
    return [
        livefeed_flightdata_dict(lfr)
        for r in results
        for lfr in livefeed_playback_response_parse(r).flights_list
    ]


def main() -> None:
    print("to be implemented")


# if __name__ == "__main__":
#     main()
#     exit(0)
#     import matplotlib.pyplot as plt

#     plt.switch_backend("QtAgg")
#     plt.style.use("dark_background")
#     df = pd.read_parquet("d91fd179-8d98-4b8b-9f8c-55d678038ff0.parquet")
#     plt.scatter(df["longitude"], df["latitude"], c="white", s=0.1, alpha=0.5)

#     for bounds in world_zones:
#         plt.plot(
#             [bounds[2], bounds[3], bounds[3], bounds[2], bounds[2]],
#             [bounds[0], bounds[0], bounds[1], bounds[1], bounds[0]],
#             c="red",
#             linewidth=0.5,
#         )
#         count = df[
#             (df["latitude"] < bounds[0])
#             & (df["latitude"] > bounds[1])
#             & (df["longitude"] > bounds[2])
#             & (df["longitude"] < bounds[3])
#         ].shape[0]
#         plt.text(
#             bounds[2],
#             bounds[0],
#             f"{count}",
#             color="red" if count > 1500 else "white",
#             fontsize=6,
#         )
#     plt.show()
