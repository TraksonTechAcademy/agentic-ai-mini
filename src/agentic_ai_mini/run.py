from __future__ import annotations

import argparse

from rich import print

from .agent import Agent
from .policies.rule_based import RuleBasedPolicy
from .tools.builtin import build_registry


TASKS = {
    "quick": "Compute 19*7 + 3.",
    "strings": "Reverse the string: 'QueenUniversity'.",
    "vowels": "Count vowels in: 'Intelligent Mining Systems'.",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a minimal agentic AI demo.")
    parser.add_argument("--task", type=str, default="quick", choices=list(TASKS.keys()))
    args = parser.parse_args()

    prompt = TASKS[args.task]
    registry = build_registry()
    policy = RuleBasedPolicy()
    agent = Agent(registry=registry, policy=policy)

    final, steps = agent.run(prompt)
    print(f"[bold]Prompt:[/bold] {prompt}")
    print(f"[bold]Final:[/bold] {final}")
    print("\n[bold]Steps:[/bold]")
    for s in steps:
        print(f"- step {s.step}: {s.action.kind}  {('tool='+s.action.tool_call.name) if s.action.tool_call else ''}")
        if s.observation is not None:
            print(f"  observation: {s.observation}")


if __name__ == "__main__":
    main()
