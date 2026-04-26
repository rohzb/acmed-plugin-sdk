# acmed-plugin-sdk

Shared plugin contract and HTTP+JSON helpers for ACMed gen2 remote issuer
plugins.

## Overview

This package provides:

- canonical request/response models used by both plugin servers and clients
- a FastAPI server scaffold with optional bearer-token auth
- a typed HTTP client for plugin contract endpoints

Canonical endpoints:

- `GET /healthz`
- `GET /capabilities`
- `POST /issue`

Core models:

- `IssueRequest`
- `IssueResult`
- `Capabilities`
- `HealthStatus`

Full contract reference:

- [`docs/plugin-api-contract.md`](docs/plugin-api-contract.md)
- Documentation index: [`docs/README.md`](docs/README.md)

Examples:

- [`examples/minimal-python-plugin`](examples/minimal-python-plugin)
- examples index: [`examples/README.md`](examples/README.md)

Plugin base image:

- Dockerfile: [`docker/base-image/Dockerfile`](docker/base-image/Dockerfile)
- docs: [`docker/base-image/README.md`](docker/base-image/README.md)

## Requirements

- Python `>=3.11`
- tested in CI on Python `3.11`, `3.12`, `3.13`, and `3.14`

## Installation

From source:

```bash
python -m pip install -e .
```

With development dependencies:

```bash
python -m pip install -e .[dev]
```

## Server Usage

Create a plugin app by implementing the handler protocol and wiring it through
`create_plugin_app`:

```python
from acmed_plugin_sdk import Capabilities, IssueRequest, IssueResult
from acmed_plugin_sdk import PluginServerSettings, create_plugin_app


class Handler:
    def capabilities(self) -> Capabilities:
        return Capabilities(
            plugin_name="example-plugin",
            plugin_version="0.1.0",
            challenge_modes=["dns-01"],
        )

    def issue(self, request: IssueRequest) -> IssueResult:
        return IssueResult(
            success=True,
            result_code="issued",
            reason_code="ok_issued",
            command="issuer-cmd",
            exit_code=0,
        )


app = create_plugin_app(
    Handler(),
    settings=PluginServerSettings(require_bearer_auth=True),
)
```

Bearer-token auth supports both current and next token environment variables:

- `ACMED_REMOTE_PLUGIN_TOKEN`
- `ACMED_REMOTE_PLUGIN_TOKEN_NEXT`

## Client Usage

Use `PluginClient` to call plugin services with typed response parsing:

```python
from acmed_plugin_sdk import IssueRequest, PluginClient

client = PluginClient(
    "http://127.0.0.1:8081",
    headers={"Authorization": "Bearer example-token"},
)

health = client.healthz()
capabilities = client.capabilities()
result = client.issue(
    IssueRequest(
        order_id="order-123",
        dns_names=["host.example.org"],
    )
)
```

## Development

```bash
python -m pip install -e .[dev]
pytest
python -m build
```

## Release and CI

- CI workflow: `.github/workflows/ci.yml`
- tag release workflow: `.github/workflows/release.yml`
- release process notes: [`RELEASE.md`](RELEASE.md)
- tagged releases also publish `ghcr.io/<owner>/acmed-plugin-base-image`

## License

MIT, see [`LICENSE`](LICENSE).
