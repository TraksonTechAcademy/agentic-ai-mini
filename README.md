# agentic-ai-mini — Minimal Agent Loop + Tool Use + Evaluation (LLM-agnostic)

This repository demonstrates **Agentic AI fundamentals** in a clean, research-ready way:

- **Agent loop**: observe → think → act → evaluate → iterate
- **Tool use**: structured tool calling with schemas and validation
- **Evaluation harness**: repeatable benchmarks + scoring + JSON outputs
- **LLM-agnostic**: you can run with a *rule-based policy* (included) or swap in an LLM later

> Designed to be high-signal for AI labs: clear abstractions, reproducibility, and measurable evaluation.

---

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Run the demo agent:
```bash
python -m agentic_ai_mini.run --task quick
```

Run the evaluation suite:
```bash
python -m agentic_ai_mini.eval --suite suites/basic.json
```

---

## What’s inside

### Agent loop (core)
- `agent.py`: agent loop + memory + tool calls
- `policies/`: how the agent chooses actions
  - `rule_based.py`: a deterministic baseline policy (no LLM)
  - `llm_stub.py`: placeholder interface for a future LLM policy

### Tools
- `tools/registry.py`: tool registry and dispatch
- `tools/builtin.py`: example tools:
  - `calculator(expr)`
  - `string_ops(mode, text)`

### Evaluation
- `suites/basic.json`: benchmark tasks
- `eval.py`: runs tasks, scores answers, saves results to `artifacts/`

---

## How to extend

1) Replace the policy with an LLM policy (or an RL policy):
- Implement `Policy.act(state) -> Action` in `policies/`

2) Add tools:
- Add a function + schema in `tools/builtin.py`
- Register it in `tools/registry.py`

3) Add benchmarks:
- Add tasks to `suites/basic.json` (and define expected outputs)

---

## Repo structure

```
agentic-ai-mini/
  suites/basic.json
  src/agentic_ai_mini/
    agent.py
    run.py
    eval.py
    schemas.py
    tools/
      registry.py
      builtin.py
    policies/
      rule_based.py
      llm_stub.py
    utils/
      io.py
      text.py
```

---

## Notes for reviewers
If you skim only 3 things:
1) `src/agentic_ai_mini/agent.py` (agent loop + tool calls)
2) `src/agentic_ai_mini/tools/registry.py` (structured tool interface)
3) `src/agentic_ai_mini/eval.py` (repeatable evaluation + scoring)

---

## License
MIT
