from app.database.security_finding_repository import SecurityFindingRepository
from app.models.security_finding import SecurityFinding
from app.models.security_finding_record import SecurityFindingRecord


class SecurityFindingPersistenceService:

    def __init__(
        self,
        repository: SecurityFindingRepository | None = None,
    ):
        self.repository = repository or SecurityFindingRepository()

    def save_finding(
        self,
        finding: SecurityFinding,
        finding_id: str,
    ) -> SecurityFindingRecord:
        record = SecurityFindingRecord(
            finding_id=finding_id,
            indicator_type=finding.indicator_type,
            file_path=finding.file_path,
            evidence=finding.evidence,
            severity=finding.severity,
            confidence=finding.confidence,
            requires_review=finding.requires_review,
            status="open",
        )

        return self.repository.create(record)