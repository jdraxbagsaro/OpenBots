# Roadmap

This is an honest snapshot, not a promise that every item will ship.

| Stage | Candidate work | Gate before release |
| --- | --- | --- |
| 0.1 | TOML configuration, mock, compatible HTTP provider, CLI, staged text workflow | Offline tests and clear setup documentation |
| 0.2 | Provider contract tests and structured request logging controls | No prompt or credential leakage in logs |
| 0.3 | Optional conversation sessions and streaming | Explicit storage lifecycle and cancellation behavior |
| Later | Opt-in tools, if there is a concrete use case | Per-tool permissions, isolation, audit trail, and threat review |

Features are not available until implemented and documented. In particular, OpenDots currently has no built-in web browsing, memory store, agent marketplace, model downloads, or shell access.