"""Canonical contract models for acmed remote issuer plugins.

The same models are used by both local and remote adapters so plugin behavior is
portable. Remote transport is HTTP+JSON in v1, but the model layer is transport
agnostic by design.

Author: ACMED Contributors
License: MIT
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

PLUGIN_API_VERSION = "1.0"
SUPPORTED_PLUGIN_API_VERSIONS = ["1.0", "0.9"]

ResultCode = Literal["issued", "issuer_error", "retryable_error"]
ReasonCode = Literal[
    "ok_issued",
    "validation_error",
    "auth_error",
    "dependency_missing",
    "dependency_failed",
    "network_error",
    "timeout",
    "rate_limited",
    "upstream_ca_error",
    "internal_error",
]


class IssueRequest(BaseModel):
    """Normalized issue call payload sent by acmed.

    Args:
        api_version: Contract version expected by the caller.
        order_id: Canonical idempotency key for one issuance intent.
        dns_names: Identifiers that must appear in the certificate SAN set.
        common_name: Optional CN when issuer tooling needs it.
        csr_pem: Optional CSR payload in PEM format.
        profile: Resolved issuer profile projection from acmed.
    """

    api_version: str = PLUGIN_API_VERSION
    order_id: str
    dns_names: list[str]
    common_name: str | None = None
    csr_pem: str | None = None
    profile: dict[str, object] = Field(default_factory=dict)

    @field_validator("order_id")
    @classmethod
    def _validate_order_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("order_id must not be empty")
        return value


class IssueResult(BaseModel):
    """Normalized issue response returned by plugin services."""

    api_version: str = PLUGIN_API_VERSION
    success: bool
    result_code: ResultCode
    reason_code: ReasonCode
    command: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    duration_ms: int | None = None
    certificate_pem: str | None = None
    chain_pem: str | None = None
    fullchain_pem: str | None = None
    private_key_pem: str | None = None


class Capabilities(BaseModel):
    """Runtime capabilities and version metadata."""

    api_version: str = PLUGIN_API_VERSION
    supported_versions: list[str] = Field(default_factory=lambda: SUPPORTED_PLUGIN_API_VERSIONS.copy())
    plugin_name: str
    plugin_version: str
    challenge_modes: list[str] = Field(default_factory=list)


class HealthStatus(BaseModel):
    """Basic plugin health state."""

    status: Literal["ok", "degraded", "failed"] = "ok"


def is_retryable_reason(reason_code: str) -> bool:
    """Return whether a reason code is retryable in v1 semantics.

    Args:
        reason_code: Contract reason-code string from plugin response.

    Returns:
        ``True`` when the reason is considered retryable by acmed policy.
    """

    return reason_code in {"timeout", "network_error", "rate_limited"}
