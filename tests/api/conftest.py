import time
from typing import Generator

import pytest


@pytest.fixture(autouse=True, scope="function")
def slow_down() -> Generator[None, None, None]:
    """Ratelimit API tests to avoid overloading the server."""

    yield
    time.sleep(2.5)
