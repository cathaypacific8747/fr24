import httpx
import pytest

from fr24.grpc import (
    follow_flight_stream,
    nearest_flights,
)
from fr24.proto import parse_data
from fr24.proto.v1_pb2 import (
    FollowFlightRequest,
    Geolocation,
    NearestFlightsRequest,
    NearestFlightsResponse,
)


# NOTE: this fixture already exists in `tests/api/conftest.py`
# TODO: remove once services are implemented
@pytest.fixture
async def nearest_flights_response(
    client: httpx.AsyncClient,
) -> NearestFlightsResponse:
    message = NearestFlightsRequest(
        location=Geolocation(lat=22.31257, lon=113.92708),
        radius=10000,
        limit=1500,
    )
    response = await nearest_flights(client, message)
    return parse_data(response.content, NearestFlightsResponse).unwrap()


@pytest.mark.anyio
async def test_follow_flight(
    nearest_flights_response: NearestFlightsResponse,
) -> None:
    flight_id = nearest_flights_response.flights_list[0].flight.flightid
    timeout = httpx.Timeout(5, read=120)
    async with httpx.AsyncClient(timeout=timeout) as client:
        message = FollowFlightRequest(flight_id=flight_id)
        i = 0
        async for response in follow_flight_stream(client, message):
            if i == 0:
                assert len(response.unwrap().flight_trail_list)
            assert response.unwrap().flight_info.flightid == flight_id
            i += 1
            if i > 2:
                break


@pytest.mark.skip(
    reason="The API began to return empty `DATA` frames since Sep 2024"
)
@pytest.mark.anyio
async def test_live_trail(
    nearest_flights_response: NearestFlightsResponse, client: httpx.AsyncClient
) -> None:
    from fr24.grpc import live_trail
    from fr24.proto.v1_pb2 import LiveTrailRequest

    flight_id = nearest_flights_response.flights_list[0].flight.flightid
    message = LiveTrailRequest(flight_id=flight_id)
    results = await live_trail(client, message)
    data = results.unwrap()
    assert len(data.radar_records_list)


@pytest.mark.skip(reason="Private API, does not return data.")
@pytest.mark.anyio
async def test_search_index(client: httpx.AsyncClient) -> None:
    from fr24.grpc import search_index
    from fr24.proto.v1_pb2 import FetchSearchIndexRequest

    message = FetchSearchIndexRequest()
    results = await search_index(client, message)
    assert results.is_ok()  # fails, empty data frame
    data = results.unwrap()
    assert data


@pytest.mark.skip(reason="Private API, does not return data.")
@pytest.mark.anyio
async def test_historic_trail(
    nearest_flights_response: NearestFlightsResponse, client: httpx.AsyncClient
) -> None:
    from fr24.grpc import historic_trail
    from fr24.proto.v1_pb2 import HistoricTrailRequest

    flight_id = nearest_flights_response.flights_list[0].flight.flightid
    message = HistoricTrailRequest(flight_id=flight_id)
    results = await historic_trail(client, message)

    assert results.is_ok()  # read timeout
    data = results.unwrap()
    from fr24.proto.v1_pb2 import HistoricTrailResponse

    assert isinstance(data, HistoricTrailResponse)


def test_parse_data_grpc_status_error() -> None:
    """Fix for: https://github.com/cathaypacific8747/fr24/issues/68"""
    from fr24.proto import GrpcError, parse_data
    from fr24.proto.v1_pb2 import FollowFlightResponse

    error_data = (
        b"\x80\x00\x00\x00/grpc-status:5\r\ngrpc-message:Flight not found!\r\n"
    )

    result = parse_data(error_data, FollowFlightResponse)

    assert result.is_err()
    err = result.err()
    assert isinstance(err, GrpcError)
    assert err.status == 5
    assert err.status_message == b"Flight not found!"
