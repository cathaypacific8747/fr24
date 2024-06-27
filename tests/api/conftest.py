import time

import pytest


@pytest.fixture(scope="module")
def slow_down():
    yield
    time.sleep(3)  # avoid overloading the server
