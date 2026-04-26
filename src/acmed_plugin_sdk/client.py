"""Typed HTTP client helpers for acmed remote issuer plugins.

This module exposes a small client used by acmed adapters and tests to
call plugin endpoints with consistent request/response validation.

The client centralizes URL building, request timeout behavior, and response
shape checks so callers do not duplicate transport glue.

Author: ACMED Contributors
License: MIT
"""

from __future__ import annotations

from typing import Any

import httpx

from .models import Capabilities, HealthStatus, IssueRequest, IssueResult


class PluginClient:
    """Simple typed client for plugin contract endpoints.

    Args:
        base_url: Base plugin URL, for example ``https://plugin.example.org``.
        timeout_seconds: Per-request timeout in seconds.
        headers: Optional headers sent with each request.
    """

    def __init__(
        self,
        base_url: str,
        timeout_seconds: int = 120,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize plugin client transport settings.

        Args:
            base_url: Base plugin URL without endpoint path.
            timeout_seconds: Per-request timeout in seconds.
            headers: Optional headers sent with every request.
        """
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._headers = headers or {}

    def _request(self, method: str, path: str, json_body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send one HTTP request and validate JSON object response shape.

        Args:
            method: HTTP method to execute.
            path: Endpoint path appended to ``base_url``.
            json_body: Optional JSON payload for request body.

        Returns:
            Parsed JSON object returned by plugin service.

        Raises:
            httpx.HTTPError: Raised by ``httpx`` on transport/status failures.
            RuntimeError: Response JSON is not an object.
        """
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
        """Fetch plugin health status.

        Returns:
            Parsed health response model.
        """

        return HealthStatus.model_validate(self._request("GET", "/healthz"))

    def capabilities(self) -> Capabilities:
        """Fetch plugin capabilities.

        Returns:
            Parsed capabilities response model.
        """

        return Capabilities.model_validate(self._request("GET", "/capabilities"))

    def issue(self, request: IssueRequest) -> IssueResult:
        """Invoke remote issuance endpoint.

        Args:
            request: Typed issuance request payload.

        Returns:
            Parsed issuance result model.
        """

        return IssueResult.model_validate(
            self._request("POST", "/issue", request.model_dump(mode="json"))
        )
