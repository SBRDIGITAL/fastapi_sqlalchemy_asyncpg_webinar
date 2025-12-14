"""Aiohttp-based client tests hitting the running FastAPI app like an external consumer."""
from __future__ import annotations

import os
from uuid import uuid4

import aiohttp
import pytest
import pytest_asyncio


def _base_url() -> str:
    host = os.getenv("API_HOST", "127.0.0.1")
    port = os.getenv("API_PORT", "8000")
    return f"http://{host}:{port}"


@pytest_asyncio.fixture()
async def client():
    async with aiohttp.ClientSession(base_url=_base_url()) as session:
        yield session


def _payload():
    return {
        "email": f"user_{uuid4()}@example.com",
        "full_name": "Test User",
        "is_hidden": False,
    }


@pytest.mark.asyncio
async def test_create_and_get_by_id(client: aiohttp.ClientSession):
    payload = _payload()
    async with client.post("/v1/users/", json=payload) as resp:
        print("create status:", resp.status)
        assert resp.status == 200 or resp.status == 201
        created = await resp.json()
        print("create body:", created)
    user_id = created["id"]

    async with client.get(f"/v1/users/{user_id}") as resp:
        print("get status:", resp.status)
        assert resp.status == 200
        fetched = await resp.json()
        print("get body:", fetched)
    assert fetched["email"] == payload["email"]
    assert fetched["full_name"] == payload["full_name"]


@pytest.mark.asyncio
async def test_list_contains_created(client: aiohttp.ClientSession):
    payload = _payload()
    async with client.post("/v1/users/", json=payload) as resp:
        print("create status:", resp.status)
        assert resp.status in (200, 201)
        created = await resp.json()
        print("create body:", created)

    async with client.get("/v1/users/") as resp:
        print("list status:", resp.status)
        assert resp.status == 200
        items = await resp.json()
        print("list body count:", len(items))
    assert any(item["id"] == created["id"] for item in items)


@pytest.mark.asyncio
async def test_get_not_found(client: aiohttp.ClientSession):
    async with client.get("/v1/users/999999999") as resp:
        print("not-found status:", resp.status)
        body = await resp.text()
        print("not-found body:", body)
        assert resp.status == 404
