"""Tests for the PointSet and Triangles binary formats."""

from __future__ import annotations

import pytest

from triangulator.binary import (
    Point,
    Triangle,
    decode_point_set,
    decode_triangles,
    encode_point_set,
    encode_triangles,
)


def test_encode_decode_point_set_roundtrip() -> None:
    points: list[Point] = [(0.0, 0.0), (1.5, -2.0), (3.25, 4.75)]
    data = encode_point_set(points)
    decoded = decode_point_set(data)

    assert len(decoded) == len(points)
    for (x1, y1), (x2, y2) in zip(points, decoded, strict=True):
        assert x2 == pytest.approx(x1)
        assert y2 == pytest.approx(y1)


def test_decode_point_set_invalid_length_raises() -> None:
    from struct import pack

    invalid = bytearray()
    invalid.extend(pack("<I", 2))
    invalid.extend(pack("<ff", 1.0, 2.0))

    with pytest.raises(ValueError):
        decode_point_set(bytes(invalid))


def test_encode_decode_triangles_roundtrip() -> None:
    points: list[Point] = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
    triangles: list[Triangle] = [(0, 1, 2), (1, 2, 3)]

    data = encode_triangles(points, triangles)
    decoded_points, decoded_triangles = decode_triangles(data)

    assert len(decoded_points) == len(points)
    for (x1, y1), (x2, y2) in zip(points, decoded_points, strict=True):
        assert x2 == pytest.approx(x1)
        assert y2 == pytest.approx(y1)

    assert decoded_triangles == triangles


def test_decode_triangles_invalid_length_raises() -> None:
    from struct import pack

    buf = bytearray()
    buf.extend(pack("<I", 1))
    buf.extend(pack("<ff", 0.0, 0.0))
    buf.extend(pack("<I", 1))
    buf.extend(pack("<I", 0))  # manque 2 indices

    with pytest.raises(ValueError):
        decode_triangles(bytes(buf))
