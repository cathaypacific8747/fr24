import httpx
import pytest

from fr24 import FR24
from fr24.service import NearestFlightsResult


@pytest.mark.anyio
async def test_follow_flight(
    nearest_flights_result: NearestFlightsResult,
) -> None:
    flight_id = (
        nearest_flights_result.to_proto().flights_list[-1].flight.flightid
    )
    timeout = httpx.Timeout(5, read=360)
    async with FR24(client=httpx.AsyncClient(timeout=timeout)) as fr24:
        i = 0
        async for result in fr24.follow_flight.stream(flight_id=flight_id):
            if i == 0:
                assert len(result.to_proto().flight_trail_list)
            assert result.to_proto().flight_info.flightid == flight_id
            i += 1
            if i > 2:
                break
