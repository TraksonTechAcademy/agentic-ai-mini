from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..schemas import Action


@dataclass
class LLMStubPolicy:
    """Placeholder interface for a future LLM policy.

    Replace `act()` with an implementation that calls your chosen LLM and returns:
    - Action(kind="tool", tool_call=...)
    - Action(kind="final", final="...")
    """

    def act(self, prompt: str, scratchpad: str) -> Action:
        # Intentionally not implemented to keep this repo API/LLM-agnostic.
        return Action(kind="final", final="LLM policy not configured.")
