from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolResult:
    tool_name: str
    success: bool
    data: Any
    error: str | None = None

    @classmethod
    def success_result(cls, tool_name: str, data: Any) -> "ToolResult":
        return cls(
            tool_name=tool_name,
            success=True,
            data=data,
        )

    @classmethod
    def error_result(cls, tool_name: str, error: str) -> "ToolResult":
        return cls(
            tool_name=tool_name,
            success=False,
            data=None,
            error=error,
        )