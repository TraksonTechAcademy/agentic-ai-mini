from __future__ import annotations

import math
import re
from typing import Literal

from pydantic import BaseModel, Field

from .registry import ToolRegistry, ToolSpec


class CalculatorArgs(BaseModel):
    expr: str = Field(..., description="A simple arithmetic expression, e.g., '19*7+3'")


def calculator(expr: str) -> str:
    # Very small safe evaluator for arithmetic expressions.
    # Allowed: digits, + - * / ( ) . and spaces
    if not re.fullmatch(r"[0-9\s\+\-\*\/\(\)\.]+", expr):
        return "[tool_error] unsupported characters in expression"
    try:
        val = eval(expr, {"__builtins__": {}}, {})
        if isinstance(val, (int, float)):
            if abs(val - int(val)) < 1e-12:
                return str(int(val))
            return str(val)
        return "[tool_error] expression did not evaluate to a number"
    except Exception as e:
        return f"[tool_error] {e}"


class StringOpsArgs(BaseModel):
    mode: Literal["reverse", "uppercase", "lowercase", "vowel_count", "strip_spaces"] = Field(...)
    text: str = Field(...)


def string_ops(mode: str, text: str) -> str:
    if mode == "reverse":
        return text[::-1]
    if mode == "uppercase":
        return text.upper()
    if mode == "lowercase":
        return text.lower()
    if mode == "strip_spaces":
        return "".join(ch for ch in text if not ch.isspace())
    if mode == "vowel_count":
        vowels = set("aeiouAEIOU")
        return str(sum(1 for ch in text if ch in vowels))
    return "[tool_error] unknown mode"


def build_registry() -> ToolRegistry:
    reg = ToolRegistry()
    reg.register(
        ToolSpec(
            name="calculator",
            description="Evaluate a basic arithmetic expression.",
            args_schema=CalculatorArgs,
            fn=calculator,
        )
    )
    reg.register(
        ToolSpec(
            name="string_ops",
            description="Simple string operations (reverse/uppercase/lowercase/vowel_count/strip_spaces).",
            args_schema=StringOpsArgs,
            fn=string_ops,
        )
    )
    return reg
