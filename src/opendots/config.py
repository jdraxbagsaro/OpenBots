"""Configuration loading and validation for OpenDots."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentConfig:
    name: str
    system_prompt: str
    max_input_chars: int


@dataclass(frozen=True)
class ProviderConfig:
    kind: str
    model: str
    base_url: str
    api_key_env: str
    timeout_seconds: float


@dataclass(frozen=True)
class AppConfig:
    agent: AgentConfig
    provider: ProviderConfig


class ConfigError(ValueError):
    """Raised when the TOML configuration is invalid."""


def load_config(path: str | Path) -> AppConfig:
    """Load and validate an OpenDots TOML configuration file."""
    config_path = Path(path)
    try:
        with config_path.open("rb") as config_file:
            raw = tomllib.load(config_file)
    except OSError as exc:
        raise ConfigError(f"Cannot read config file: {config_path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"Invalid TOML in {config_path}: {exc}") from exc

    try:
        agent_raw = raw["agent"]
        provider_raw = raw["provider"]
        agent = AgentConfig(
            name=_required_string(agent_raw, "name"),
            system_prompt=_required_string(agent_raw, "system_prompt"),
            max_input_chars=int(agent_raw.get("max_input_chars", 12000)),
        )
        provider = ProviderConfig(
            kind=_required_string(provider_raw, "kind"),
            model=_required_string(provider_raw, "model"),
            base_url=str(provider_raw.get("base_url", "http://127.0.0.1:11434/v1")),
            api_key_env=str(provider_raw.get("api_key_env", "OPENDOTS_API_KEY")),
            timeout_seconds=float(provider_raw.get("timeout_seconds", 60)),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ConfigError(f"Invalid configuration value: {exc}") from exc

    if agent.max_input_chars < 1:
        raise ConfigError("agent.max_input_chars must be greater than zero")
    if provider.kind not in {"mock", "openai-compatible"}:
        raise ConfigError("provider.kind must be 'mock' or 'openai-compatible'")
    if provider.timeout_seconds <= 0:
        raise ConfigError("provider.timeout_seconds must be greater than zero")
    if provider.kind == "openai-compatible" and not provider.base_url.startswith(("http://", "https://")):
        raise ConfigError("provider.base_url must use http:// or https://")

    return AppConfig(agent=agent, provider=provider)


def api_key_for(config: ProviderConfig) -> str | None:
    """Read a provider API key from the configured environment variable."""
    if not config.api_key_env:
        return None
    return os.environ.get(config.api_key_env) or None


def _required_string(section: dict[str, object], key: str) -> str:
    value = section[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()
