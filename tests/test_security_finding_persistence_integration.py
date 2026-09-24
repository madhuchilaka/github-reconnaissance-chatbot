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


def test_security_finding_can_be_persisted():
    repository = FakeSecurityFindingRepository()
    service = SecurityFindingPersistenceService(repository)

    finding = SecurityFinding(
        indicator_type="AWS_ACCESS_KEY",
        file_path="config.py",
        evidence="AKIA********************",
        severity="critical",
        confidence=0.98,
        requires_review=True,
    )

    result = service.save_finding(
        finding=finding,
        finding_id="finding-aws-001",
    )

    assert result.finding_id == "finding-aws-001"
    assert result.indicator_type == "AWS_ACCESS_KEY"
    assert result.file_path == "config.py"
    assert result.evidence == "AKIA********************"
    assert result.severity == "critical"
    assert result.confidence == 0.98
    assert result.requires_review is True
    assert result.status == "open"

    assert repository.created_records == [result]