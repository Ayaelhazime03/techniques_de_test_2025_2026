"""Tests for the HTTP API exposed by the Triangulator service."""

from __future__ import annotations

import pytest
from flask.testing import FlaskClient

from triangulator.app import create_app
from triangulator.binary import decode_triangles, encode_point_set
from triangulator.pointset_client import (
    PointSetManagerUnavailableError,
    PointSetNotFoundError,
)


def _make_uuid() -> str:
    return "123e4567-e89b-12d3-a456-426614174000"


class _FakeClient:
    """Simple fake PointSetManager client for API tests."""

    def __init__(self, data: bytes | None = None, error: Exception | None = None) -> None:
        self.data = data
        self.error = error

    def get_point_set(self, point_set_id: str) -> bytes:
        if self.error is not None:
            raise self.error
        assert self.data is not None
        return self.data


def test_get_triangulation_happy_path() -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    point_set_bytes = encode_point_set(points)
    fake_client = _FakeClient(data=point_set_bytes)

    app = create_app(client=fake_client)
    test_client: FlaskClient = app.test_client()

    response = test_client.get(f"/triangulation/{_make_uuid()}")

    assert response.status_code == 200
    assert response.mimetype == "application/octet-stream"

    vertices, triangles = decode_triangles(response.data)
    assert len(vertices) == len(points)
    assert len(triangles) == 1
    assert set(triangles[0]) == {0, 1, 2}


def test_get_triangulation_invalid_uuid_returns_400() -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    point_set_bytes = encode_point_set(points)
    fake_client = _FakeClient(data=point_set_bytes)

    app = create_app(client=fake_client)
    test_client: FlaskClient = app.test_client()

    response = test_client.get("/triangulation/not-a-uuid")

    assert response.status_code == 400
    body = response.get_json()
    assert body["code"] == "INVALID_POINTSET_ID"


def test_get_triangulation_404_when_pointset_not_found() -> None:
    fake_client = _FakeClient(error=PointSetNotFoundError("not found"))
    app = create_app(client=fake_client)
    test_client: FlaskClient = app.test_client()

    response = test_client.get(f"/triangulation/{_make_uuid()}")

    assert response.status_code == 404
    body = response.get_json()
    assert body["code"] == "POINTSET_NOT_FOUND"


def test_get_triangulation_503_when_pointset_manager_unavailable() -> None:
    fake_client = _FakeClient(error=PointSetManagerUnavailableError("down"))
    app = create_app(client=fake_client)
    test_client: FlaskClient = app.test_client()

    response = test_client.get(f"/triangulation/{_make_uuid()}")

    assert response.status_code == 503
    body = response.get_json()
    assert body["code"] == "POINTSET_MANAGER_UNAVAILABLE"


def test_get_triangulation_invalid_pointset_binary_returns_500() -> None:
    from struct import pack

    broken = bytearray()
    broken.extend(pack("<I", 2))
    broken.extend(pack("<ff", 0.0, 0.0))

    fake_client = _FakeClient(data=bytes(broken))
    app = create_app(client=fake_client)
    test_client: FlaskClient = app.test_client()

    response = test_client.get(f"/triangulation/{_make_uuid()}")

    assert response.status_code == 500
    body = response.get_json()
    assert body["code"] == "INVALID_POINTSET_FORMAT"


def test_get_triangulation_triangulation_failure_returns_500(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    point_set_bytes = encode_point_set(points)
    fake_client = _FakeClient(data=point_set_bytes)

    app = create_app(client=fake_client)
    test_client: FlaskClient = app.test_client()

    def fake_triangulate(_points):
        raise RuntimeError("boom")

    monkeypatch.setattr("triangulator.app.triangulate", fake_triangulate)

    response = test_client.get(f"/triangulation/{_make_uuid()}")

    assert response.status_code == 500
    body = response.get_json()
    assert body["code"] == "TRIANGULATION_FAILED"
