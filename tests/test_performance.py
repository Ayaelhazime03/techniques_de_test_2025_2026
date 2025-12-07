"""Performance tests for the Triangulator service."""

from __future__ import annotations

import random
import time

import pytest

from triangulator.binary import decode_point_set, encode_point_set, encode_triangles
from triangulator.delaunay import triangulate


def _random_points(n: int, seed: int = 42) -> list[tuple[float, float]]:
    random.seed(seed)
    return [(random.random(), random.random()) for _ in range(n)]


@pytest.mark.perf
def test_perf_encode_decode_point_set() -> None:
    points = _random_points(10_000)

    start = time.perf_counter()
    data = encode_point_set(points)
    mid = time.perf_counter()
    _ = decode_point_set(data)
    end = time.perf_counter()

    print(f"encode_point_set(10k): {mid - start:.4f}s")
    print(f"decode_point_set(10k): {end - mid:.4f}s")


@pytest.mark.perf
def test_perf_triangulate_medium_point_set() -> None:
    points = _random_points(1_000)

    start = time.perf_counter()
    triangles = triangulate(points)
    end = time.perf_counter()

    print(f"triangulate(1000): {end - start:.4f}s, produced {len(triangles)} triangles")


@pytest.mark.perf
def test_perf_triangles_encoding() -> None:
    points = _random_points(2_000)
    triangles = triangulate(points)

    start = time.perf_counter()
    _ = encode_triangles(points, triangles)
    end = time.perf_counter()

    print(f"encode_triangles(2000 points, {len(triangles)} triangles): {end - start:.4f}s")
