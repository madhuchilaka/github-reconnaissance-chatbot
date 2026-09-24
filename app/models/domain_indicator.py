from dataclasses import dataclass


@dataclass(frozen=True)
class DomainIndicator:
    domain: str
    evidence: list[str]