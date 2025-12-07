"""Flask application exposing the Triangulator HTTP API."""

from __future__ import annotations

import os
import uuid
from typing import Optional

from flask import Flask, Response, jsonify

from .binary import decode_point_set, encode_triangles
from .delaunay import triangulate
from .pointset_client import (
    PointSetError,
    PointSetManagerClient,
    PointSetManagerUnavailableError,
    PointSetNotFoundError,
)


def create_app(client: Optional[PointSetManagerClient] = None) -> Flask:
    """Application factory for the Triangulator Flask app."""
    app = Flask(__name__)
    app.config["POINT_SET_CLIENT"] = client or PointSetManagerClient()

    @app.route("/triangulation/<point_set_id>", methods=["GET"])
    def get_triangulation(point_set_id: str) -> Response:
        """Handle GET /triangulation/{pointSetId} requests."""
        # 1. Vérifier que point_set_id est un UUID valide
        try:
            uuid.UUID(point_set_id)
        except (ValueError, AttributeError):
            return (
                jsonify(
                    {
                        "code": "INVALID_POINTSET_ID",
                        "message": "pointSetId must be a valid UUID.",
                    },
                ),
                400,
            )

        client_obj: PointSetManagerClient = app.config["POINT_SET_CLIENT"]

        # 2. Récupérer le PointSet auprès du PointSetManager
        try:
            point_set_bytes = client_obj.get_point_set(point_set_id)
        except PointSetNotFoundError as exc:
            return (
                jsonify(
                    {
                        "code": "POINTSET_NOT_FOUND",
                        "message": str(exc),
                    },
                ),
                404,
            )
        except PointSetManagerUnavailableError as exc:
            return (
                jsonify(
                    {
                        "code": "POINTSET_MANAGER_UNAVAILABLE",
                        "message": str(exc),
                    },
                ),
                503,
            )
        except PointSetError as exc:
            return (
                jsonify(
                    {
                        "code": "POINTSET_MANAGER_ERROR",
                        "message": str(exc),
                    },
                ),
                503,
            )

        # 3. Décoder le PointSet binaire
        try:
            points = decode_point_set(point_set_bytes)
        except ValueError as exc:
            return (
                jsonify(
                    {
                        "code": "INVALID_POINTSET_FORMAT",
                        "message": str(exc),
                    },
                ),
                500,
            )

        # 4. Trianguler
        try:
            triangles = triangulate(points)
        except Exception as exc:  # pragma: no cover (défensif)
            return (
                jsonify(
                    {
                        "code": "TRIANGULATION_FAILED",
                        "message": f"Triangulation failed: {exc}",
                    },
                ),
                500,
            )

        # 5. Encoder le résultat dans le format binaire Triangles
        triangles_bytes = encode_triangles(points, triangles)
        return Response(
            triangles_bytes,
            status=200,
            mimetype="application/octet-stream",
        )

    return app


# Application par défaut si on fait `python -m triangulator.app`
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("TRIANGULATOR_PORT", "5002"))
    app.run(host="0.0.0.0", port=port)
