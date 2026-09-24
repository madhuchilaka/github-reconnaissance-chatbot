import pytest

from app.models.security_finding_record import SecurityFindingRecord
from app.services.security_finding_status_service import (
    update_finding_status,
    update_finding_statuses,
)

def make_record(status: str = "open") -> SecurityFindingRecord:
    return SecurityFindingRecord(
        finding_id="finding-001",
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
        status=status,
    )


def test_open_to_reviewed():
    record = make_record("open")

    updated = update_finding_status(record, "reviewed")

    assert updated.status == "reviewed"
    assert updated.finding_id == record.finding_id


def test_reviewed_to_resolved():
    record = make_record("reviewed")

    updated = update_finding_status(record, "resolved")

    assert updated.status == "resolved"


def test_reviewed_to_false_positive():
    record = make_record("reviewed")

    updated = update_finding_status(record, "false_positive")

    assert updated.status == "false_positive"


def test_invalid_status_transition_is_rejected():
    record = make_record("open")

    with pytest.raises(ValueError):
        update_finding_status(record, "resolved")


def test_resolved_record_cannot_be_reopened():
    record = make_record("resolved")

    with pytest.raises(ValueError):
        update_finding_status(record, "open")



def test_update_finding_statuses():
    records = [
        make_record("open"),
        SecurityFindingRecord(
            finding_id="finding-002",
            indicator_type="AWS_SECRET_KEY",
            file_path="config/aws.py",
            evidence="AWS_********************",
            severity="critical",
            confidence=0.98,
            requires_review=True,
            status="reviewed",
        ),
    ]

    updated_records = update_finding_statuses(
        records,
        {
            "finding-001": "reviewed",
            "finding-002": "resolved",
        },
    )

    assert len(updated_records) == 2
    assert updated_records[0].status == "reviewed"
    assert updated_records[1].status == "resolved"