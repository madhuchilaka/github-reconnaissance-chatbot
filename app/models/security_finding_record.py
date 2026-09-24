from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityFindingRecord:
    finding_id: str
    indicator_type: str
    file_path: str
    evidence: str
    severity: str
    confidence: float
    requires_review: bool
    status: str



