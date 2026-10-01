# Security and trust boundaries

OpenDots is a small starter project, not a sandbox or a security certification. Treat it as a client that sends prompts to a model endpoint.

## Current guarantees and limits

| Area | Current behavior | Important limitation |
| --- | --- | --- |
| Local input handling | Rejects empty messages and enforces a character limit | Character count is not a token, cost, or abuse control |
| Credentials | Reads an optional bearer token from an environment variable | Environment variables may be visible to processes or diagnostic tools on your machine |
| Tool access | No tools are implemented or enabled | Adding tools later will require explicit permissions and isolation |
| Network | Sends requests only when the HTTP provider is selected and used | The selected server receives the system prompt, objective, and workflow stage context |
| Model behavior | System prompt is sent as ordinary provider input | A prompt is not a security boundary and does not guarantee model behavior |
| Workflow | Runs three model calls sequentially and returns all stage outputs | Intermediate outputs are sent back to the provider in later calls |

## Operator checklist

- Prefer a loopback-only listener for local inference unless remote access is intentional.
- Use HTTPS and a narrowly scoped token when connecting across a network.
- Do not put secrets, personal data, or confidential prompts into a server you do not control.
- Keep `opendots.toml`, `.env`, and credentials out of version control.
- Review the model and server licenses, data-handling behavior, and acceptable-use terms yourself.
- Do not expose an inference endpoint to the public internet without appropriate authentication, rate limits, and network controls.

OpenDots adds no separate output moderation layer. That does not disable safeguards implemented by a model or provider, and local hosting does not automatically mean safe, private, unrestricted, or free of model-license obligations.