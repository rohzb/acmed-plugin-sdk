"""Minimal example plugin handler.

This implementation is intentionally simple and returns normalized responses
without invoking external issuance tools.
"""

from __future__ import annotations

from acmed_plugin_sdk.models import Capabilities, IssueRequest, IssueResult


class ExamplePlugin:
    """Minimal plugin that always returns a controlled failure."""

    def capabilities(self) -> Capabilities:
        return Capabilities(
            plugin_name="acmed-issuer-example",
            plugin_version="0.1.0",
            challenge_modes=["dns-01"],
        )

    def issue(self, request: IssueRequest) -> IssueResult:
        return IssueResult(
            success=False,
            result_code="issuer_error",
            reason_code="internal_error",
            command=f"example-plugin issue order_id={request.order_id}",
            exit_code=65,
            stderr="example plugin does not issue certificates; copy and customize this handler",
        )
