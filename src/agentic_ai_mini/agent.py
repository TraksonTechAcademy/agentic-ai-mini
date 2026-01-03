from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .schemas import Action, StepResult
from .tools.registry import ToolRegistry


@dataclass
class AgentState:
    prompt: str
    scratchpad: str = ""
    steps: int = 0


class Agent:
    def __init__(self, registry: ToolRegistry, policy) -> None:
        self.registry = registry
        self.policy = policy

    def run(self, prompt: str, max_steps: int = 6) -> tuple[str, List[StepResult]]:
        state = AgentState(prompt=prompt)
        history: List[StepResult] = []

        for step in range(1, max_steps + 1):
            state.steps = step
            action: Action = self.policy.act(state.prompt, state.scratchpad)

            if action.kind == "final":
                final = action.final or ""
                history.append(StepResult(step=step, action=action, observation=None))
                return final, history

            if action.kind == "think":
                thought = action.thought or ""
                state.scratchpad += f"[thought] {thought}\n"
                history.append(StepResult(step=step, action=action, observation=None))
                continue

            # Tool call
            if action.kind == "tool" and action.tool_call is not None:
                obs = self.registry.call(action.tool_call.name, action.tool_call.arguments)
                # Special: allow multi-step composition for a demo pattern
                if action.tool_call.name == "string_ops" and action.tool_call.arguments.get("mode") == "uppercase":
                    state.scratchpad += f"uppercased={obs}\n"
                state.scratchpad += f"[observation] {obs}\n"
                history.append(StepResult(step=step, action=action, observation=obs))
                continue

        return "(max_steps reached)", history
