from __future__ import annotations

import pytest

from acmed_plugin_sdk.models import IssueRequest, is_retryable_reason


def test_issue_request_requires_non_empty_order_id():
    with pytest.raises(ValueError):
        IssueRequest(order_id="  ", dns_names=["host.example.org"])


def test_issue_request_normalizes_order_id():
    request = IssueRequest(order_id="  order-1  ", dns_names=["host.example.org"])
    assert request.order_id == "order-1"


@pytest.mark.parametrize("reason_code", ["timeout", "network_error", "rate_limited"])
def test_is_retryable_reason_true(reason_code: str):
    assert is_retryable_reason(reason_code) is True


@pytest.mark.parametrize("reason_code", ["ok_issued", "validation_error", "internal_error", "other"])
def test_is_retryable_reason_false(reason_code: str):
    assert is_retryable_reason(reason_code) is False
