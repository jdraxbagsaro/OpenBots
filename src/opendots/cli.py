"""Command-line interface for OpenDots."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from opendots import __version__
from opendots.config import AppConfig, ConfigError, api_key_for, load_config
from opendots.providers import ProviderError
from opendots.runtime import Agent
from opendots.workflow import Workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="opendots",
        description="Run a configurable AI agent against a local or compatible chat endpoint.",
    )
    parser.add_argument("--version", action="version", version=f"OpenDots {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="send one message to the configured agent")
    run_parser.add_argument("--config", "-c", default="opendots.toml", help="TOML config path")
    run_parser.add_argument("--message", "-m", required=True, help="message to send")

    workflow_parser = subparsers.add_parser(
        "workflow", help="run a visible plan, compose, and review sequence"
    )
    workflow_parser.add_argument("--config", "-c", default="opendots.toml", help="TOML config path")
    workflow_parser.add_argument("--objective", "-g", required=True, help="objective for the workflow")
    workflow_parser.add_argument("--format", choices=("text", "json"), default="text")

    doctor_parser = subparsers.add_parser("doctor", help="validate config and provider setup")
    doctor_parser.add_argument("--config", "-c", default="opendots.toml", help="TOML config path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        config = load_config(Path(args.config))
        if args.command == "doctor":
            _doctor(config)
            return
        agent = Agent(config, api_key=api_key_for(config.provider))
        if args.command == "workflow":
            result = Workflow(agent.respond).run(args.objective)
            if args.format == "json":
                print(json.dumps(result.to_dict(), indent=2))
            else:
                for stage in result.stages:
                    print(f"## {stage.stage.title()}\n{stage.output}\n")
            return
        print(agent.respond(args.message))
    except (ConfigError, ProviderError, ValueError) as exc:
        print(f"opendots: error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


def _doctor(config: AppConfig) -> None:
    provider = config.provider
    print(f"Configuration: valid")
    print(f"Agent: {config.agent.name}")
    print(f"Provider: {provider.kind} ({provider.model})")
    if provider.kind == "openai-compatible":
        key_present = bool(api_key_for(provider))
        print(f"API key environment variable {provider.api_key_env}: {'set' if key_present else 'not set'}")
        print(f"Endpoint: {provider.base_url.rstrip('/')}/chat/completions")
        print("Network connectivity: not checked")
    else:
        print("Mock mode: no model server or credentials required")


if __name__ == "__main__":
    main()
