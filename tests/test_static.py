import pytest
from pydantic import TypeAdapter

from fr24.static import (
    get_aircraft_family,
    get_airlines,
    get_airports,
    get_countries,
)
from fr24.types.static import (
    AircraftFamily,
    Airlines,
    Airports,
    Countries,
    StaticData,
)


@pytest.mark.parametrize(
    "data,typed_dict",
    [
        (get_aircraft_family(), AircraftFamily),
        (get_airlines(), Airlines),
        (get_airports(), Airports),
        (get_countries(), Countries),
    ],
)
def test_static_types(data: StaticData, typed_dict: StaticData) -> None:
    ta = TypeAdapter(typed_dict)  # type: ignore[var-annotated]
    ta.validate_python(data)
