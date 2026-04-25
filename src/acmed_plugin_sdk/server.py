"""FastAPI server scaffold for acmed remote issuer plugins.

This module standardizes endpoint behavior and optional service-token
authentication so plugin services do not have to re-implement it.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from fastapi import Depends, FastAPI, Header, HTTPException, status

from .models import Capabilities, HealthStatus, IssueRequest, IssueResult


class PluginHandler(Protocol):
    """Interface implemented by concrete issuer plugins."""

    def capabilities(self) -> Capabilities: ...

    def issue(self, request: IssueRequest) -> IssueResult: ...


@dataclass(slots=True)
class PluginServerSettings:
    """Runtime behavior for plugin HTTP server wrapper."""

    require_bearer_auth: bool = True
    token_env_var: str = "ACMED_REMOTE_PLUGIN_TOKEN"
    token_next_env_var: str = "ACMED_REMOTE_PLUGIN_TOKEN_NEXT"


def _build_auth_dependency(settings: PluginServerSettings) -> Callable[..., None]:
    """Create auth dependency callable based on settings."""

    def _no_auth() -> None:
        return None

    def _auth(authorization: str | None = Header(default=None)) -> None:
        token = os.environ.get(settings.token_env_var, "").strip()
        next_token = os.environ.get(settings.token_next_env_var, "").strip()
        accepted = [value for value in [next_token, token] if value]
        if not accepted:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "plugin token is not configured in environment: "
                    f"{settings.token_env_var} or {settings.token_next_env_var}"
                ),
            )
        if authorization not in {f"Bearer {value}" for value in accepted}:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid or missing bearer token",
            )

    return _auth if settings.require_bearer_auth else _no_auth


def create_plugin_app(
    handler: PluginHandler,
    settings: PluginServerSettings | None = None,
) -> FastAPI:
    """Create a FastAPI app exposing canonical plugin endpoints."""

    resolved = settings or PluginServerSettings()
    auth = _build_auth_dependency(resolved)
    app = FastAPI(title="acmed plugin service", version="0.2.0")

    @app.get("/healthz", response_model=HealthStatus)
    def healthz() -> HealthStatus:
        return HealthStatus(status="ok")

    @app.get("/capabilities", response_model=Capabilities, dependencies=[Depends(auth)])
    def capabilities() -> Capabilities:
        return handler.capabilities()

    @app.post("/issue", response_model=IssueResult, dependencies=[Depends(auth)])
    def issue(request: IssueRequest) -> IssueResult:
        return handler.issue(request)

    return app
