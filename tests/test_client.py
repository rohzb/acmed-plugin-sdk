from __future__ import annotations

import httpx
import pytest

from acmed_plugin_sdk.client import PluginClient
from acmed_plugin_sdk.models import IssueRequest


class _Response:
    def __init__(self, payload, status_exc: Exception | None = None):
        self._payload = payload
        self._status_exc = status_exc

    def raise_for_status(self) -> None:
        if self._status_exc is not None:
            raise self._status_exc

    def json(self):
        return self._payload


def test_client_healthz_capabilities_and_issue(monkeypatch):
    calls: list[tuple[str, str, int, dict[str, str], dict | None]] = []

    def _fake_request(method, url, timeout, headers, json):  # noqa: ANN001
        calls.append((method, url, timeout, headers, json))
        if url.endswith("/healthz"):
            return _Response({"status": "ok"})
        if url.endswith("/capabilities"):
            return _Response(
                {
                    "api_version": "1.0",
                    "supported_versions": ["1.0", "0.9"],
                    "plugin_name": "test-plugin",
                    "plugin_version": "0.1.0",
                    "challenge_modes": ["dns-01"],
                }
            )
        if url.endswith("/issue"):
            return _Response(
                {
                    "api_version": "1.0",
                    "success": True,
                    "result_code": "issued",
                    "reason_code": "ok_issued",
                    "command": "issuer",
                    "exit_code": 0,
                    "stdout": "",
                    "stderr": "",
                }
            )
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(httpx, "request", _fake_request)
    client = PluginClient("https://plugin.example.org/", timeout_seconds=9, headers={"Authorization": "Bearer t"})

    health = client.healthz()
    capabilities = client.capabilities()
    issue = client.issue(IssueRequest(order_id="order-1", dns_names=["host.example.org"]))

    assert health.status == "ok"
    assert capabilities.plugin_name == "test-plugin"
    assert issue.success is True
    assert issue.result_code == "issued"

    assert calls[0] == ("GET", "https://plugin.example.org/healthz", 9, {"Authorization": "Bearer t"}, None)
    assert calls[1] == ("GET", "https://plugin.example.org/capabilities", 9, {"Authorization": "Bearer t"}, None)
    assert calls[2][0] == "POST"
    assert calls[2][1] == "https://plugin.example.org/issue"
    assert calls[2][2] == 9
    assert calls[2][3] == {"Authorization": "Bearer t"}
    assert calls[2][4] == {
        "api_version": "1.0",
        "order_id": "order-1",
        "dns_names": ["host.example.org"],
        "common_name": None,
        "csr_pem": None,
        "profile": {},
    }


def test_client_raises_for_non_object_payload(monkeypatch):
    def _fake_request(method, url, timeout, headers, json):  # noqa: ANN001, ARG001
        return _Response(["not-an-object"])

    monkeypatch.setattr(httpx, "request", _fake_request)
    client = PluginClient("https://plugin.example.org")

    with pytest.raises(RuntimeError, match="non-object JSON payload"):
        client.healthz()


def test_client_bubbles_http_errors(monkeypatch):
    request = httpx.Request("GET", "https://plugin.example.org/healthz")
    response = httpx.Response(status_code=401, request=request)
    status_exc = httpx.HTTPStatusError("unauthorized", request=request, response=response)

    def _fake_request(method, url, timeout, headers, json):  # noqa: ANN001, ARG001
        return _Response({"status": "failed"}, status_exc=status_exc)

    monkeypatch.setattr(httpx, "request", _fake_request)
    client = PluginClient("https://plugin.example.org")

    with pytest.raises(httpx.HTTPStatusError):
        client.healthz()
