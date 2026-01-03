from __future__ import annotations

import argparse
import time
import yaml
import json
import os
from typing import Dict, Any, List

from rich import print

from .agent import Agent
from .policies.rule_based import RuleBasedPolicy
from .tools.builtin import build_registry
from .utils.io import write_json


def score_exact(pred: str, expected: str) -> float:
    return 1.0 if pred.strip() == expected.strip() else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate agent on a deterministic suite.")
    parser.add_argument("--suite", type=str, default="suites/basic.json")
    parser.add_argument("--out_dir", type=str, default="artifacts")
    args = parser.parse_args()

    with open(args.suite, "r", encoding="utf-8") as f:
        suite = json.load(f)

    registry = build_registry()
    policy = RuleBasedPolicy()
    agent = Agent(registry=registry, policy=policy)

    results: List[Dict[str, Any]] = []
    passed = 0
    total = len(suite["tasks"])

    ts = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"eval-{suite['name']}-{ts}"

    for task in suite["tasks"]:
        final, steps = agent.run(task["prompt"])
        sc = score_exact(final, task["expected"])
        passed += int(sc == 1.0)
        results.append(
            {
                "id": task["id"],
                "prompt": task["prompt"],
                "expected": task["expected"],
                "pred": final,
                "score": sc,
                "steps": [s.model_dump() for s in steps],
            }
        )
        print(f"[bold]{task['id']}[/bold] score={sc}  pred='{final}' expected='{task['expected']}'")

    summary = {
        "suite": suite["name"],
        "run_id": run_id,
        "passed": passed,
        "total": total,
        "accuracy": passed / max(1, total),
        "results": results,
    }

    out_path = os.path.join(args.out_dir, f"{run_id}.json")
    write_json(out_path, summary)
    print(f"\n[green]Saved:[/green] {out_path}")
    print(f"[bold]Accuracy:[/bold] {summary['accuracy']:.2%}")


if __name__ == "__main__":
    main()
