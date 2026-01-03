from __future__ import annotations

from typing import Any, Dict, Optional, Literal, List
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    name: str = Field(..., description="Tool name to call")
    arguments: Dict[str, Any] = Field(default_factory=dict)


class Action(BaseModel):
    kind: Literal["tool", "final", "think"] = "think"
    tool_call: Optional[ToolCall] = None
    final: Optional[str] = None
    thought: Optional[str] = None


class StepResult(BaseModel):
    step: int
    action: Action
    observation: Optional[str] = None


class EpisodeResult(BaseModel):
    task_id: str
    prompt: str
    final_answer: str
    steps: List[StepResult]
    score: float
    passed: bool
