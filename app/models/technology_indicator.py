from dataclasses import dataclass


@dataclass(frozen=True)
class TechnologyIndicator:
    name: str
    category: str
    evidence: list[str]