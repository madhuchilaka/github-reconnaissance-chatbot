from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityIndicator:
    indicator_type: str
    file_path: str
    evidence: str
