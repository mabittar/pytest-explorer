from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from httpx import ASGITransport
from httpx import AsyncClient
from src.core.calculator import Calculator
from src.main import app


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@pytest.fixture(scope="class")
def valid_calc_input():
    return Calculator(2, 3)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="module")
def json_data():
    return {"a": 1, "b": 2}


@pytest.fixture
def json_headers():
    return {"Content-Type": "application/json"}
