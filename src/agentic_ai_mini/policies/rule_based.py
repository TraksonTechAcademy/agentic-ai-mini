from __future__ import annotations

import re
from dataclasses import dataclass

from ..schemas import Action, ToolCall


@dataclass
class RuleBasedPolicy:
    """Deterministic baseline policy (no LLM).

    It detects a few task patterns and chooses tools accordingly.
    This is useful for:
      - verifying the agent loop + tool interface
      - providing a baseline in evaluation
    """

    def act(self, prompt: str, scratchpad: str) -> Action:
        # If we already have a tool observation in scratchpad, finalize using it.
        if "[observation]" in scratchpad:
            # Take the last observation line as the final answer.
            last = scratchpad.strip().splitlines()[-1]
            obs = last.replace("[observation]", "").strip()
            return Action(kind="final", final=obs)

        # Calculator: detect "Compute ..." and extract expression-like content.
        m = re.search(r"Compute\s+(.+?)(\.|$)", prompt, re.IGNORECASE)
        if m:
            expr = m.group(1).strip()
            # normalize common punctuation
            expr = expr.replace("×", "*").replace("÷", "/")
            return Action(kind="tool", tool_call=ToolCall(name="calculator", arguments={"expr": expr}))

        # Reverse string: "Reverse the string: '...'" 
        m = re.search(r"Reverse\s+the\s+string:\s*'([^']+)'", prompt, re.IGNORECASE)
        if m:
            return Action(kind="tool", tool_call=ToolCall(name="string_ops", arguments={"mode":"reverse", "text": m.group(1)}))

        # Count vowels: "Count vowels in: '...'" or in: "...."
        m = re.search(r"Count\s+vowels\s+in:\s*'([^']+)'", prompt, re.IGNORECASE)
        if m:
            return Action(kind="tool", tool_call=ToolCall(name="string_ops", arguments={"mode":"vowel_count", "text": m.group(1)}))

        # Uppercase then reverse: "Uppercase then reverse: 'agentic'."
        m = re.search(r"Uppercase\s+then\s+reverse:\s*'([^']+)'", prompt, re.IGNORECASE)
        if m:
            # We'll do this in two steps: uppercase, then reverse.
            # Step 1: uppercase
            if "uppercased=" not in scratchpad:
                return Action(kind="tool", tool_call=ToolCall(name="string_ops", arguments={"mode":"uppercase", "text": m.group(1)}))
            # Step 2: reverse the cached uppercased result
            upper = scratchpad.split("uppercased=")[-1].splitlines()[0].strip()
            return Action(kind="tool", tool_call=ToolCall(name="string_ops", arguments={"mode":"reverse", "text": upper}))

        return Action(kind="final", final="(no rule matched)")
