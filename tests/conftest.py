# mypy: ignore-errors
import time

import pytest

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(autouse=True)
def slow_down():
    yield
    time.sleep(2)  # avoid overloading the server
