from __future__ import annotations

import pytest

from acmed_plugin_sdk.models import IssueRequest


def test_issue_request_requires_non_empty_order_id():
    with pytest.raises(ValueError):
        IssueRequest(order_id="  ", dns_names=["host.example.org"])
