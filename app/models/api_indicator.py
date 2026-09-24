from dataclasses import dataclass


@dataclass(frozen=True)
class ApiIndicator:
    url: str
    method: str | None
    evidence: list[str]
