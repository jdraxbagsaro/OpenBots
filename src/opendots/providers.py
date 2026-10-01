"""Provider implementations used by the agent runtime."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from opendots.config import ProviderConfig


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


class ProviderError(RuntimeError):
    """Raised when a provider request fails or returns an invalid response."""


class MockProvider:
    """Deterministic provider for demos and offline smoke tests."""

    def complete(self, messages: list[ChatMessage]) -> str:
        user_message = next(message.content for message in reversed(messages) if message.role == "user")
        return f"[OpenDots mock] Received your message: {user_message}"


class OpenAICompatibleProvider:
    """Minimal adapter for local servers exposing the chat-completions API."""

    def __init__(self, config: ProviderConfig, api_key: str | None = None) -> None:
        self.config = config
        self.api_key = api_key

    def complete(self, messages: list[ChatMessage]) -> str:
        endpoint = f"{self.config.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in messages
            ],
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ProviderError(f"Provider request failed: {exc}") from exc

        try:
            content = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Provider returned an unexpected chat-completions response") from exc
        if not isinstance(content, str):
            raise ProviderError("Provider response content was not text")
        return content


def create_provider(config: ProviderConfig, api_key: str | None = None) -> MockProvider | OpenAICompatibleProvider:
    if config.kind == "mock":
        return MockProvider()
    return OpenAICompatibleProvider(config, api_key=api_key)
