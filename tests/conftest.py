"""Pytest fixtures for the Triangulator tests."""

from __future__ import annotations

import pytest
from flask import Flask

from triangulator.app import create_app
from triangulator.pointset_client import PointSetManagerClient


class FakePointSetClient(PointSetManagerClient):
    """Fake client used in tests to avoid real HTTP calls."""

    def __init__(self, data: bytes | None = None, error: Exception | None = None) -> None:
        super().__init__(base_url="http://fake")
        self._data = data
        self._error = error

    def get_point_set(self, point_set_id: str) -> bytes:
        if self._error is not None:
            raise self._error
        assert self._data is not None, "FakePointSetClient has no data configured."
        return self._data


@pytest.fixture
def app() -> Flask:
    """Return a Flask app configured with a dummy client by default."""
    return create_app()

