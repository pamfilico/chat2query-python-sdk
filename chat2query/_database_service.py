"""Internal database service used by Chat2QueryService."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from chat2query.exceptions import APIError


class _DatabaseService:
    """Encapsulates database CRUD operations for Chat2QueryService."""

    def __init__(self, sdk_service: "Chat2QueryService"):
        self._service = sdk_service

    def list(self) -> List[Dict[str, Any]]:
        """Fetch all databases for the authenticated user."""
        response = self._service._request("GET", "/api/v1/database")
        data = response.get("data")
        if data is None:
            raise APIError("Database list response did not include data")
        if not isinstance(data, list):
            raise APIError("Database list response was not a list")
        return data

    def get(self, database_id: int) -> Dict[str, Any]:
        """Retrieve a single database by id."""
        response = self._service._request("GET", f"/api/v1/database/{database_id}")
        data = response.get("data")
        if data is None:
            raise APIError("Database response did not include data")
        if not isinstance(data, dict):
            raise APIError("Database response was not an object")
        return data

    def create(
        self,
        *,
        name: str,
        database_uri: str,
        description: Optional[str] = None,
    ) -> Any:
        """Create a new database record."""
        payload: Dict[str, Any] = {
            "name": name,
            "database_uri": database_uri,
            "description": description,
        }
        response = self._service._request("POST", "/api/v1/database", data=payload)
        return response.get("data")

    def update(
        self,
        database_id: int,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        database_uri: Optional[str] = None,
    ) -> Any:
        """Update database metadata."""
        payload = {
            key: value
            for key, value in {
                "name": name,
                "description": description,
                "database_uri": database_uri,
            }.items()
            if value is not None
        }
        if not payload:
            raise APIError("At least one field must be provided to update a database")

        response = self._service._request(
            "PUT", f"/api/v1/database/{database_id}", data=payload
        )
        return response.get("data")

    def delete(self, database_id: int) -> None:
        """Deleting databases is restricted to the web application."""
        raise APIError("Deleting databases is only available in the web application.")

    def generate_description(
        self, database_id: int, *, model: Optional[str] = None
    ) -> str:
        """
        Request a generated description for the database.

        Args:
            database_id: Identifier of the database to describe.
            model: Optional model name to delegate to (defaults to server-side default).

        Returns:
            The generated description text.
        """
        payload: Dict[str, Any] = {}
        if model:
            payload["model"] = model
        response = self._service._request(
            "POST",
            f"/api/v1/database/{database_id}/generate-description",
            data=payload or None,
        )
        data = response.get("data") or {}
        description = data.get("description")
        if description is None:
            raise APIError("Generate description response missing description field")
        return description
