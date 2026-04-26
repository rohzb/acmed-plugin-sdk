"""FastAPI entrypoint for the minimal plugin example."""

from __future__ import annotations

from acmed_issuer_example.plugin import ExamplePlugin
from acmed_plugin_sdk.server import PluginServerSettings, create_plugin_app

app = create_plugin_app(
    ExamplePlugin(),
    settings=PluginServerSettings(require_bearer_auth=True),
)
