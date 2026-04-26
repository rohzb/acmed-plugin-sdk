# ACMED Plugin API Contract (v1)

This document defines the HTTP+JSON contract for ACMED remote issuer plugins.
It describes API version 1 (v1).
It is the canonical interface reference for plugin implementers and acmed
integrators.

## Scope

- Transport: HTTP/1.1 or HTTP/2
- Payload format: JSON
- Base path: `/`
- Canonical endpoints:
  - `GET /healthz`
  - `GET /capabilities`
  - `POST /issue`

## Versioning

- API generation: `v1`
- Current API version: `1.0`
- Supported API versions: `["1.0", "0.9"]`
- Request and response payloads include `api_version`.
- Plugins should return `api_version: "1.0"` for the current contract.

## Authentication

`/capabilities` and `/issue` can require bearer auth (default behavior in SDK
server scaffold).

Accepted token environment variables:

- `ACMED_REMOTE_PLUGIN_TOKEN`
- `ACMED_REMOTE_PLUGIN_TOKEN_NEXT`

Authorization header format:

```text
Authorization: Bearer <token>
```

Auth failure behavior in the default server scaffold:

- `503 Service Unavailable` when auth is enabled but no token env var is set
- `401 Unauthorized` when token is missing/invalid

`/healthz` is always unauthenticated in the default scaffold.

## Endpoint Contract

### `GET /healthz`

Purpose: service liveness/readiness probe.

Response `200 OK`:

```json
{
  "status": "ok"
}
```

`status` enum:

- `ok`
- `degraded`
- `failed`

### `GET /capabilities`

Purpose: discover plugin identity and supported challenge modes.

Response `200 OK`:

```json
{
  "api_version": "1.0",
  "supported_versions": ["1.0", "0.9"],
  "plugin_name": "example-plugin",
  "plugin_version": "0.2.0",
  "challenge_modes": ["dns-01"]
}
```

Fields:

- `api_version` (`string`)
- `supported_versions` (`array[string]`)
- `plugin_name` (`string`)
- `plugin_version` (`string`)
- `challenge_modes` (`array[string]`)

Typical auth-related errors:

- `401 Unauthorized`
- `503 Service Unavailable`

### `POST /issue`

Purpose: execute one issuance attempt for a resolved order intent.

Request body:

```json
{
  "api_version": "1.0",
  "order_id": "order-123",
  "dns_names": ["host.example.org"],
  "common_name": null,
  "csr_pem": null,
  "profile": {}
}
```

Request fields:

- `api_version` (`string`, default `1.0`)
- `order_id` (`string`, required, non-empty after trim)
- `dns_names` (`array[string]`, required)
- `common_name` (`string | null`)
- `csr_pem` (`string | null`)
- `profile` (`object`, default `{}`)

Response `200 OK`:

```json
{
  "api_version": "1.0",
  "success": true,
  "result_code": "issued",
  "reason_code": "ok_issued",
  "command": "issuer-cmd",
  "exit_code": 0,
  "stdout": "",
  "stderr": "",
  "duration_ms": 1234,
  "certificate_pem": null,
  "chain_pem": null,
  "fullchain_pem": null,
  "private_key_pem": null
}
```

Response fields:

- `api_version` (`string`)
- `success` (`boolean`)
- `result_code` (`"issued" | "issuer_error" | "retryable_error"`)
- `reason_code`:
  - `ok_issued`
  - `validation_error`
  - `auth_error`
  - `dependency_missing`
  - `dependency_failed`
  - `network_error`
  - `timeout`
  - `rate_limited`
  - `upstream_ca_error`
  - `internal_error`
- `command` (`string`)
- `exit_code` (`integer`)
- `stdout` (`string`)
- `stderr` (`string`)
- `duration_ms` (`integer | null`)
- `certificate_pem` (`string | null`)
- `chain_pem` (`string | null`)
- `fullchain_pem` (`string | null`)
- `private_key_pem` (`string | null`)

Typical auth-related errors:

- `401 Unauthorized`
- `503 Service Unavailable`

Validation errors are returned as framework-level request validation responses
(for example when required fields are missing or malformed).

## Result Semantics

`reason_code` values considered retryable by current SDK helper policy:

- `timeout`
- `network_error`
- `rate_limited`

This mapping is exposed by `is_retryable_reason(reason_code: str) -> bool`.

## Compatibility Rules

- Additive fields are preferred for backward compatibility.
- Existing field names and meanings must remain stable within a major contract
  version.
- Breaking changes require a new contract version and coordinated rollout.

## Reference Implementation

SDK contract/model sources:

- `src/acmed_plugin_sdk/models.py`
- `src/acmed_plugin_sdk/server.py`
- `src/acmed_plugin_sdk/client.py`
