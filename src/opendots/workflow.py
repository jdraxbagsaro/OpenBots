"""A transparent, text-only multi-stage workflow for agent responses."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable


@dataclass(frozen=True)
class WorkflowStage:
    name: str
    instruction: str


@dataclass(frozen=True)
class StageResult:
    stage: str
    output: str


@dataclass(frozen=True)
class WorkflowResult:
    objective: str
    stages: tuple[StageResult, ...]

    @property
    def final_output(self) -> str:
        return self.stages[-1].output

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


DEFAULT_STAGES = (
    WorkflowStage(
        name="plan",
        instruction=(
            "Break the objective into concise subgoals. State key assumptions and "
            "observable completion checks. Do not claim external actions were performed."
        ),
    ),
    WorkflowStage(
        name="compose",
        instruction=(
            "Draft a useful response using the objective and the previous stage output. "
            "Separate known facts from assumptions and identify missing context."
        ),
    ),
    WorkflowStage(
        name="review",
        instruction=(
            "Review the draft for unsupported claims, omissions, and unclear wording. "
            "Return a corrected final response and brief review notes. Do not claim "
            "that external actions or tests were performed."
        ),
    ),
)


class Workflow:
    """Run a fixed, inspectable sequence using an injected text responder."""

    def __init__(
        self,
        respond: Callable[[str], str],
        stages: tuple[WorkflowStage, ...] = DEFAULT_STAGES,
    ) -> None:
        if not stages:
            raise ValueError("A workflow must contain at least one stage")
        if len({stage.name for stage in stages}) != len(stages):
            raise ValueError("Workflow stage names must be unique")
        self.respond = respond
        self.stages = stages

    def run(self, objective: str) -> WorkflowResult:
        if not objective.strip():
            raise ValueError("Workflow objective must not be empty")

        results: list[StageResult] = []
        previous_output: str | None = None
        for stage in self.stages:
            prompt = (
                f"Objective:\n{objective}\n\n"
                f"Current stage: {stage.name}\n"
                f"Instruction: {stage.instruction}"
            )
            if previous_output is not None:
                prompt += f"\n\nPrevious stage output:\n{previous_output}"
            output = self.respond(prompt)
            results.append(StageResult(stage=stage.name, output=output))
            previous_output = output

        return WorkflowResult(objective=objective, stages=tuple(results))