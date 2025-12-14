"""Интеграционные тесты для роутера пользователей API v1.

Используем FastAPI TestClient для синхронного тестирования с поддержкой lifespan.
"""
from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def client():
    """Создает TestClient для тестирования FastAPI приложения с lifespan."""
    with TestClient(app) as test_client:
        yield test_client


def _create_user_payload():
    return {
        "email": f"user_{uuid4()}@example.com",
        "full_name": "Test User",
        "is_hidden": False,
    }


def test_create_user_and_get_by_id(client: TestClient):
    payload = _create_user_payload()

    resp_create = client.post("/v1/users/", json=payload)
    assert resp_create.status_code in (200, 201)
    created = resp_create.json()
    user_id = created["id"]

    assert created["email"] == payload["email"]
    assert created["full_name"] == payload["full_name"]
    assert created["is_hidden"] is payload["is_hidden"]

    resp_get = client.get(f"/v1/users/{user_id}")
    assert resp_get.status_code == 200
    fetched = resp_get.json()

    assert fetched["id"] == user_id
    assert fetched["email"] == payload["email"]
    assert fetched["full_name"] == payload["full_name"]


def test_get_all_contains_created_user(client: TestClient):
    payload = _create_user_payload()
    resp_create = client.post("/v1/users/", json=payload)
    assert resp_create.status_code in (200, 201)
    created = resp_create.json()

    resp_all = client.get("/v1/users/")
    assert resp_all.status_code == 200
    all_users = resp_all.json()
    assert any(u["id"] == created["id"] for u in all_users)


def test_get_by_id_not_found(client: TestClient):
    resp = client.get("/v1/users/999999999")
    assert resp.status_code == 404
