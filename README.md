# acmed-plugin-sdk

Shared plugin contract and transport helpers for acmed gen2.

## Contract

Remote plugin endpoints:

- `GET /healthz`
- `GET /capabilities`
- `POST /issue`

Core models:

- `IssueRequest`
- `IssueResult`
- `Capabilities`
- `HealthStatus`

## Server scaffold

Use `create_plugin_app(handler, settings=...)` to create a plugin API service
with optional bearer-token enforcement.

Token auth supports both current and next token environment variables:

- `ACMED_REMOTE_PLUGIN_TOKEN`
- `ACMED_REMOTE_PLUGIN_TOKEN_NEXT`

## Client

Use `PluginClient` from core-side adapters or integration tests to call plugin
services with typed request/response parsing.

## Release and CI

- CI workflow: `.github/workflows/ci.yml`
- Tag release workflow: `.github/workflows/release.yml`
- Release process notes: [`RELEASE.md`](RELEASE.md)

## Local validation

```bash
python -m pip install -e .[dev]
pytest
python -m build
```
