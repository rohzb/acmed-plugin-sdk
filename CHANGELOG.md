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

### Changed
- Expanded Python module/class/function docstrings to improve maintainability and
  generated documentation quality.
- Release workflow now gates on successful CI using the shared
  `rohzb/ci-actions/wait-for-workflows` action.
- Core GitHub Actions in CI/release are pinned to immutable commit SHAs.
