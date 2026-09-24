from app.models.security_finding import SecurityFinding


def test_security_finding_fields():
    finding = SecurityFinding(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
    )

    assert finding.indicator_type == "GITHUB_TOKEN"
    assert finding.file_path == "config/github.py"
    assert finding.evidence == "ghp_********************"
    assert finding.severity == "high"
    assert finding.confidence == 0.95
    assert finding.requires_review is True


def test_security_finding_is_immutable():
    finding = SecurityFinding(
        indicator_type="AWS_ACCESS_KEY",
        file_path="config/aws.py",
        evidence="AWS_********************",
        severity="high",
        confidence=0.90,
        requires_review=True,
    )

    try:
        finding.severity = "low"
    except AttributeError:
        pass
    else:
        raise AssertionError("SecurityFinding should be immutable")