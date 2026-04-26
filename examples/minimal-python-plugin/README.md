# Minimal Python Plugin Example

This is a copy-and-modify template for new remote issuer plugins.

## Build

From `upstream/acmed_gen2/acmed-plugin-sdk`:

```bash
docker build -f examples/minimal-python-plugin/Dockerfile -t acmed-issuer-example:0.1.0 .
```

## Next steps

1. Replace `ExamplePlugin.issue()` with your issuer tool execution logic.
2. Return normalized `IssueResult` fields, including `result_code` and `reason_code`.
3. Keep `order_id` idempotency behavior deterministic.
