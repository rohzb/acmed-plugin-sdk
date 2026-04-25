# Release Process

## Versioning

- Tags follow `vX.Y.Z`.
- `pyproject.toml` version must match the tag without `v`.

## Checklist

1. Run tests and package build locally.
2. Update `CHANGELOG.md`.
3. Bump version in `pyproject.toml` if needed.
4. Commit and push branch.
5. Create and push tag (`vX.Y.Z`).

## Automation

Tag push triggers `.github/workflows/release.yml` and creates:

- Python artifacts (`sdist` + wheel)
- GitHub release with attached dist files
- Optional PyPI publish when `PYPI_API_TOKEN` secret is configured
