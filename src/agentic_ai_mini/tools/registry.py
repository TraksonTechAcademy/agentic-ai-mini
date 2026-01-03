from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Any

from pydantic import BaseModel, ValidationError


@dataclass
class ToolSpec:
    name: str
    description: str
    args_schema: type[BaseModel]
    fn: Callable[..., str]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def list_tools(self) -> Dict[str, ToolSpec]:
        return dict(self._tools)

    def call(self, name: str, arguments: Dict[str, Any]) -> str:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        spec = self._tools[name]
        try:
            parsed = spec.args_schema(**arguments)
        except ValidationError as e:
            return f"[tool_error] invalid arguments for '{name}': {e}"
        try:
            return spec.fn(**parsed.model_dump())
        except Exception as e:
            return f"[tool_error] exception in '{name}': {e}"
