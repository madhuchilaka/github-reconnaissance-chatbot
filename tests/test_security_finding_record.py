from app.models.security_finding_record import SecurityFindingRecord


def test_security_finding_record_fields():
    record = SecurityFindingRecord(
        finding_id="finding-001",
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
        status="open",
    )

    assert record.finding_id == "finding-001"
    assert record.indicator_type == "GITHUB_TOKEN"
    assert record.file_path == "config/github.py"
    assert record.evidence == "ghp_********************"
    assert record.severity == "high"
    assert record.confidence == 0.95
    assert record.requires_review is True
    assert record.status == "open"


def test_security_finding_record_is_immutable():
    record = SecurityFindingRecord(
        finding_id="finding-002",
        indicator_type="AWS_SECRET_KEY",
        file_path="config/aws.py",
        evidence="AWS_********************",
        severity="critical",
        confidence=0.98,
        requires_review=True,
        status="open",
    )

    try:
        record.status = "resolved"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "SecurityFindingRecord should be immutable"
        )