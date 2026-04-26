FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG ACMED_PLUGIN_SDK_SPEC=acmed-plugin-sdk>=0.2.0
ARG ACMED_PLUGIN_SDK_FALLBACK=

WORKDIR /opt/plugin

RUN pip install --no-cache-dir "${ACMED_PLUGIN_SDK_SPEC}" \
    || (test -n "${ACMED_PLUGIN_SDK_FALLBACK}" && pip install --no-cache-dir "${ACMED_PLUGIN_SDK_FALLBACK}")

EXPOSE 8081
