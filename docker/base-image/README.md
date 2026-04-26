# Plugin Base Image

Reusable runtime base image for ACMED remote plugin services.

## Purpose

- install Python runtime dependencies shared by plugin services
- include `acmed-plugin-sdk` server/client contract package
- provide a small base layer that plugin images can extend

## Build

From `acmed-plugin-sdk` repository root:

```bash
docker build -f docker/base-image/Dockerfile -t acmed-plugin-base:0.2.0 .
```

Optional SDK source override:

```bash
docker build -f docker/base-image/Dockerfile \
  --build-arg ACMED_PLUGIN_SDK_SPEC='acmed-plugin-sdk>=0.2.0' \
  --build-arg ACMED_PLUGIN_SDK_FALLBACK='https://example.org/acmed-plugin-sdk-0.2.0.tar.gz' \
  -t acmed-plugin-base:0.2.0 .
```
