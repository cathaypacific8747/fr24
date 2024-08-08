import time
from typing import Generator

import pytest


@pytest.fixture(autouse=True, scope="function")
def slow_down() -> Generator[None, None, None]:
    yield
    time.sleep(2.5)  # avoid overloading the server
