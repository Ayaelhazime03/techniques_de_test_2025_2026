"""Tests for the Delaunay triangulation algorithm."""

from __future__ import annotations

from triangulator.delaunay import triangulate


def test_triangulate_simple_triangle() -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = triangulate(points)

    assert len(triangles) == 1
    assert set(triangles[0]) == {0, 1, 2}


def test_triangulate_square_produces_two_triangles() -> None:
    points = [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
    ]
    triangles = triangulate(points)

    assert len(triangles) == 2
    used_vertices = {idx for tri in triangles for idx in tri}
    assert used_vertices == {0, 1, 2, 3}


def test_triangulate_returns_empty_for_less_than_three_points() -> None:
    assert triangulate([]) == []
    assert triangulate([(0.0, 0.0)]) == []
    assert triangulate([(0.0, 0.0), (1.0, 0.0)]) == []


def test_triangulate_collinear_points_returns_empty() -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    triangles = triangulate(points)
    assert triangles == []
