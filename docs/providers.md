# Providers

## Offline mock

Set `provider.kind = "mock"` to test configuration, CLI wiring, and input limits without network access. The mock returns a labeled echo; it is not intelligent, and it must not be used to evaluate an agent prompt or model quality.

## OpenAI-compatible chat completions

Set `provider.kind = "openai-compatible"`. OpenDots sends one JSON `POST` request to `{base_url}/chat/completions` with `model` and a `messages` array. The expected response contains `choices[0].message.content` as text.

Example:

```toml
[provider]
kind = "openai-compatible"
model = "your-server-model-id"
base_url = "http://127.0.0.1:11434/v1"
api_key_env = "OPENDOTS_API_KEY"
timeout_seconds = 60
```

The configured base URL should include any API prefix, such as `/v1`, but not the `/chat/completions` path itself. OpenDots does not probe the endpoint during `doctor`; that command validates local setup and reports that network connectivity was not checked.

The `workflow` command sends three requests sequentially to the configured provider. The objective and intermediate output are included in later stage prompts, so request volume, latency, and transmitted data are higher than for `run`.

### Compatibility notes

- Servers may differ in model identifiers, authentication, timeouts, and supported request fields.
- The initial adapter does not expose temperature, token limits, streaming, retries, or custom headers.
- TLS and authentication behavior are controlled by Python's standard HTTP stack and the server configuration.
- A provider may apply its own safety rules, data retention, or usage policy. OpenDots cannot remove or override them.