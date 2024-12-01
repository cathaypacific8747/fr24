import httpx
import pytest
import pytest_asyncio

from fr24.grpc import (
    follow_flight_request_create,
    follow_flight_stream,
    live_flights_status_post,
    live_flights_status_request_create,
    nearest_flights_post,
    nearest_flights_request_create,
    top_flights_post,
    top_flights_request_create,
)
from fr24.proto.v1_pb2 import (
    FollowFlightRequest,
    Geolocation,
    LiveFlightsStatusRequest,
    NearestFlightsRequest,
    NearestFlightsResponse,
    Status,
    TopFlightsRequest,
)


@pytest_asyncio.fixture(scope="function")
async def nearest_flights() -> NearestFlightsResponse:
    async with httpx.AsyncClient() as client:
        message = NearestFlightsRequest(
            location=Geolocation(lat=22.31257, lon=113.92708),
            radius=10000,
            limit=1500,
        )
        request = nearest_flights_request_create(message)
        data = await nearest_flights_post(client, request)
        return data


@pytest.mark.asyncio
async def test_nearest_flights(
    nearest_flights: NearestFlightsResponse,
) -> None:
    assert len(nearest_flights.flights_list) > 5


@pytest.mark.asyncio
async def test_live_flights_status(
    nearest_flights: NearestFlightsResponse,
) -> None:
    flight_ids = [f.flight.flightid for f in nearest_flights.flights_list]

    async with httpx.AsyncClient() as client:
        message = LiveFlightsStatusRequest(flight_ids_list=flight_ids[:3])
        request = live_flights_status_request_create(message)
        data_status = await live_flights_status_post(client, request)
        assert len(data_status.flights_map) == 3
        for flight in data_status.flights_map:
            assert flight.data.status == Status.LIVE


@pytest.mark.asyncio
async def test_follow_flight(
    nearest_flights: NearestFlightsResponse,
) -> None:
    flight_id = nearest_flights.flights_list[0].flight.flightid
    timeout = httpx.Timeout(5, read=120)
    async with httpx.AsyncClient(timeout=timeout) as client:
        message = FollowFlightRequest(flight_id=flight_id)
        request = follow_flight_request_create(message)
        i = 0
        async for response in follow_flight_stream(client, request):
            if i == 0:
                assert len(response.flight_trail_list)
            assert response.flight_info.flightid == flight_id
            i += 1
            if i > 2:
                break


@pytest.mark.asyncio
async def test_top_flights() -> None:
    async with httpx.AsyncClient() as client:
        message = TopFlightsRequest(limit=10)
        request = top_flights_request_create(message)
        top_flights = await top_flights_post(client, request)
        assert len(top_flights.scoreboard_list)


# NOTE: the api has failed to return any data since Sep 2024.
# @pytest.mark.asyncio
# async def test_live_trail(nearest_flights: NearestFlightsResponse) -> None:
#     flight_id = nearest_flights.flights_list[0].flight.flightid
#     async with httpx.AsyncClient() as client:
#         message = LiveTrailRequest(flight_id=flight_id)
#         request = live_trail_request_create(message)
#         data = await live_trail_post(client, request)
#         assert len(data.radar_records_list)
