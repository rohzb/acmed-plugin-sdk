from __future__ import annotations

from fastapi.testclient import TestClient

from acmed_plugin_sdk.models import Capabilities, IssueRequest, IssueResult
from acmed_plugin_sdk.server import PluginServerSettings, create_plugin_app


class _Handler:
    def capabilities(self) -> Capabilities:
        return Capabilities(plugin_name="test", plugin_version="0.1.0", challenge_modes=["dns-01"])

    def issue(self, request: IssueRequest) -> IssueResult:
        return IssueResult(
            success=True,
            result_code="issued",
            reason_code="ok_issued",
            command="noop",
            exit_code=0,
            certificate_pem="CERT",
            fullchain_pem="FULLCHAIN",
            private_key_pem="KEY",
        )


def test_server_accepts_current_or_next_bearer_token(monkeypatch):
    monkeypatch.setenv("ACMED_REMOTE_PLUGIN_TOKEN", "cur")
    monkeypatch.setenv("ACMED_REMOTE_PLUGIN_TOKEN_NEXT", "next")

    app = create_plugin_app(_Handler(), settings=PluginServerSettings(require_bearer_auth=True))
    client = TestClient(app)

    cur = client.get("/capabilities", headers={"Authorization": "Bearer cur"})
    nxt = client.get("/capabilities", headers={"Authorization": "Bearer next"})
    bad = client.get("/capabilities", headers={"Authorization": "Bearer bad"})

    assert cur.status_code == 200
    assert nxt.status_code == 200
    assert bad.status_code == 401


def test_server_returns_503_when_auth_enabled_but_tokens_missing(monkeypatch):
    monkeypatch.delenv("ACMED_REMOTE_PLUGIN_TOKEN", raising=False)
    monkeypatch.delenv("ACMED_REMOTE_PLUGIN_TOKEN_NEXT", raising=False)

    app = create_plugin_app(_Handler(), settings=PluginServerSettings(require_bearer_auth=True))
    client = TestClient(app)

    response = client.get("/capabilities")
    assert response.status_code == 503
    assert "plugin token is not configured" in response.json()["detail"]


def test_server_can_disable_auth_and_issue_endpoint_works(monkeypatch):
    # Ensure no token env is needed when auth is disabled.
    monkeypatch.delenv("ACMED_REMOTE_PLUGIN_TOKEN", raising=False)
    monkeypatch.delenv("ACMED_REMOTE_PLUGIN_TOKEN_NEXT", raising=False)

    app = create_plugin_app(_Handler(), settings=PluginServerSettings(require_bearer_auth=False))
    client = TestClient(app)

    health = client.get("/healthz")
    capabilities = client.get("/capabilities")
    issue = client.post(
        "/issue",
        json={
            "order_id": "order-1",
            "dns_names": ["host.example.org"],
        },
    )

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert capabilities.status_code == 200
    assert capabilities.json()["plugin_name"] == "test"
    assert issue.status_code == 200
    assert issue.json()["result_code"] == "issued"
