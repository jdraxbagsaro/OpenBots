"""Agent orchestration kept independent from provider transport."""

from __future__ import annotations

from opendots.config import AppConfig
from opendots.policy import validate_input
from opendots.providers import ChatMessage, create_provider


class Agent:
    def __init__(self, config: AppConfig, api_key: str | None = None) -> None:
        self.config = config
        self.provider = create_provider(config.provider, api_key=api_key)

    def respond(self, message: str) -> str:
        validate_input(message, self.config.agent.max_input_chars)
        messages = [
            ChatMessage(role="system", content=self.config.agent.system_prompt),
            ChatMessage(role="user", content=message),
        ]
        return self.provider.complete(messages)
