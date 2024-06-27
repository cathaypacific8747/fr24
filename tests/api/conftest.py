import time

import pytest


@pytest.fixture(autouse=True, scope="function")
def slow_down():
    yield
    time.sleep(2.5)  # avoid overloading the server
