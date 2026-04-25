"""Typed HTTP client helpers for acmed remote issuer plugins."""

from __future__ import annotations

from typing import Any

import httpx

from .models import Capabilities, HealthStatus, IssueRequest, IssueResult


class PluginClient:
    """Simple typed client for plugin contract endpoints."""

    def __init__(
        self,
        base_url: str,
        timeout_seconds: int = 120,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._headers = headers or {}

    def _request(self, method: str, path: str, json_body: dict[str, Any] | None = None) -> dict[str, Any]:
        response = httpx.request(
            method,
            f"{self._base_url}{path}",
            timeout=self._timeout_seconds,
            headers=self._headers,
            json=json_body,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise RuntimeError("plugin returned non-object JSON payload")
        return data

    def healthz(self) -> HealthStatus:
        """Fetch plugin health status."""

        return HealthStatus.model_validate(self._request("GET", "/healthz"))

    def capabilities(self) -> Capabilities:
        """Fetch plugin capabilities."""

        return Capabilities.model_validate(self._request("GET", "/capabilities"))

    def issue(self, request: IssueRequest) -> IssueResult:
        """Invoke remote issuance endpoint."""

        return IssueResult.model_validate(
            self._request("POST", "/issue", request.model_dump(mode="json"))
        )
