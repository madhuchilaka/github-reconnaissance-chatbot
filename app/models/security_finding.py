from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityFinding:
    indicator_type: str
    file_path: str
    evidence: str
    severity: str
    confidence: float
    requires_review: bool