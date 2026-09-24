from app.models.security_finding import SecurityFinding
from app.services.security_finding_record_service import (
    create_security_finding_record,
    create_security_finding_records,
)


def test_create_security_finding_record():
    finding = SecurityFinding(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
    )

    record = create_security_finding_record(
        finding=finding,
        finding_id="finding-001",
    )

    assert record.finding_id == "finding-001"
    assert record.indicator_type == "GITHUB_TOKEN"
    assert record.file_path == "config/github.py"
    assert record.evidence == "ghp_********************"
    assert record.severity == "high"
    assert record.confidence == 0.95
    assert record.requires_review is True
    assert record.status == "open"


def test_create_security_finding_record_defaults_to_open():
    finding = SecurityFinding(
        indicator_type="AWS_SECRET_KEY",
        file_path="config/aws.py",
        evidence="AWS_********************",
        severity="critical",
        confidence=0.98,
        requires_review=True,
    )

    record = create_security_finding_record(
        finding=finding,
        finding_id="finding-002",
    )

    assert record.status == "open"


def test_create_security_finding_records():
    findings = [
        SecurityFinding(
            indicator_type="GITHUB_TOKEN",
            file_path="config/github.py",
            evidence="ghp_********************",
            severity="high",
            confidence=0.95,
            requires_review=True,
        ),
        SecurityFinding(
            indicator_type="AWS_SECRET_KEY",
            file_path="config/aws.py",
            evidence="AWS_********************",
            severity="critical",
            confidence=0.98,
            requires_review=True,
        ),
    ]

    records = create_security_finding_records(
        findings=findings,
        finding_ids=["finding-001", "finding-002"],
    )

    assert len(records) == 2
    assert records[0].finding_id == "finding-001"
    assert records[0].indicator_type == "GITHUB_TOKEN"
    assert records[0].status == "open"

    assert records[1].finding_id == "finding-002"
    assert records[1].indicator_type == "AWS_SECRET_KEY"
    assert records[1].severity == "critical"
    assert records[1].status == "open"