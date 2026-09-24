from app.models.security_finding import SecurityFinding
from app.models.security_finding_record import SecurityFindingRecord
from app.services.security_finding_persistence_service import (
    SecurityFindingPersistenceService,
)


class FakeSecurityFindingRepository:

    def __init__(self):
        self.created_records = []

    def create(
        self,
        record: SecurityFindingRecord,
    ) -> SecurityFindingRecord:
        self.created_records.append(record)
        return record


def test_save_finding_creates_security_finding_record():
    repository = FakeSecurityFindingRepository()
    service = SecurityFindingPersistenceService(repository)

    finding = SecurityFinding(
        indicator_type="GITHUB_TOKEN",
        file_path=".env",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
    )

    result = service.save_finding(
        finding=finding,
        finding_id="finding-001",
    )

    expected = SecurityFindingRecord(
        finding_id="finding-001",
        indicator_type="GITHUB_TOKEN",
        file_path=".env",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
        status="open",
    )

    assert result == expected
    assert repository.created_records == [expected]