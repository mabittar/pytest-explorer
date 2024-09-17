from __future__ import annotations

from json import loads

import pytest

from fastapi import status


@pytest.mark.anyio(backend="asyncio")
async def test_add(client, json_headers, json_data):
    response = await client.post("/api/add/", headers=json_headers, json=json_data)
    assert response.status_code == status.HTTP_200_OK
    response_text = loads(response.text)
    assert response_text["result"] == 3


@pytest.mark.anyio(backend="asyncio")
async def test_subtract(client, json_headers, json_data):
    response = await client.post("/api/subtract/", headers=json_headers, json=json_data)
    assert response.status_code == status.HTTP_200_OK
    response_text = loads(response.text)
    assert response_text["result"] == -1


@pytest.mark.anyio(backend="asyncio")
async def test_multiply(client, json_headers, json_data):
    response = await client.post("/api/multiply/", headers=json_headers, json=json_data)
    assert response.status_code == status.HTTP_200_OK
    response_text = loads(response.text)
    assert response_text["result"] == 2


@pytest.mark.anyio(backend="asyncio")
async def test_divide_by_zero(client, json_headers):
    divide_data = {"a": 1, "b": 0}
    response = await client.post("/api/divide/", headers=json_headers, json=divide_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
