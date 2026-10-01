# Project principles

OpenDots is an independently developed open-source project. It is designed around configurable personal-agent workflows and is not affiliated with any external platform.

The project follows the broad personal-agent idea: a configurable assistant can take a user's objective through a repeatable workflow. OpenDots implements that idea as a local-first CLI runtime with provider adapters and a visible `plan → compose → review` sequence. It does not claim feature parity with any hosted agent product.

| Statement | Meaning in this repository |
| --- | --- |
| Free | The OpenDots software is MIT-licensed and free to use; model inference, hardware, and hosting may cost money |
| No OpenDots-side censorship | This runtime adds no separate content moderation or output-filtering stage |
| Uncensored | Not a guarantee about model output; the selected model or provider may apply its own safeguards |
| Agent workflow | Three sequential text completions; no autonomous browser, shell, or computer actions |

Capabilities are described according to the code that ships. OpenDots is its own project, implementation, and roadmap.