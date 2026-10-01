from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from opendots.config import ConfigError, load_config
from opendots.policy import InputLimitError
from opendots.runtime import Agent
from opendots.workflow import Workflow


class RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "opendots.toml"
        self.config_path.write_text(
            '[agent]\nname = "Test Agent"\nsystem_prompt = "Be concise."\nmax_input_chars = 12\n\n'
            '[provider]\nkind = "mock"\nmodel = "demo"\n',
            encoding="utf-8",
        )
        self.config = load_config(self.config_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_mock_provider_returns_explicit_demo_response(self) -> None:
        response = Agent(self.config).respond("hello")
        self.assertEqual(response, "[OpenDots mock] Received your message: hello")

    def test_input_limit_is_enforced_before_provider_call(self) -> None:
        with self.assertRaises(InputLimitError):
            Agent(self.config).respond("this message is too long")

    def test_unknown_provider_is_rejected(self) -> None:
        self.config_path.write_text(
            '[agent]\nname = "Test Agent"\nsystem_prompt = "Be concise."\n\n'
            '[provider]\nkind = "unknown"\nmodel = "demo"\n',
            encoding="utf-8",
        )
        with self.assertRaises(ConfigError):
            load_config(self.config_path)

    def test_workflow_passes_each_stage_output_forward(self) -> None:
        prompts: list[str] = []

        def responder(prompt: str) -> str:
            prompts.append(prompt)
            return f"stage-{len(prompts)}"

        result = Workflow(responder).run("Prepare a project brief")

        self.assertEqual([stage.stage for stage in result.stages], ["plan", "compose", "review"])
        self.assertEqual(result.final_output, "stage-3")
        self.assertIn("Previous stage output:\nstage-1", prompts[1])
        self.assertIn("Previous stage output:\nstage-2", prompts[2])

    def test_workflow_rejects_empty_objective_before_calling_responder(self) -> None:
        calls: list[str] = []
        with self.assertRaises(ValueError):
            Workflow(calls.append).run("  ")
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()