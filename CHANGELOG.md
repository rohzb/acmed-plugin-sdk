# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-04-26

### Added
- Canonical plugin contract models (`IssueRequest`, `IssueResult`, `Capabilities`, `HealthStatus`).
- Typed HTTP client and FastAPI server scaffolding for remote issuer plugins.
- Bearer token auth support with current+next token acceptance.
- CI and release workflows for automated package validation and publishing.
- Dedicated API contract reference doc at `docs/plugin-api-contract.md`.
- Release notes document at `docs/releases/v0.2.0.md`.
- In-repo examples under `examples/`, including `examples/minimal-python-plugin`.
- In-repo plugin base image under `docker/base-image/`.

### Changed
- Expanded Python module/class/function docstrings to improve maintainability and
  generated documentation quality.
- Release workflow now gates on successful CI using the shared
  `rohzb/ci-actions/wait-for-workflows` action.
- CI/release GitHub Actions are pinned to immutable commit SHAs, including
  Docker and publish/release actions.
- Release workflow now builds and publishes `ghcr.io/<owner>/acmed-plugin-base-image` on tag releases.
