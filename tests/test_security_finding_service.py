from app.models.security_indicator import SecurityIndicator
from app.services.security_finding_service import build_security_finding


def test_build_security_finding_redacts_evidence():
    indicator = SecurityIndicator(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_1234567890abcdefghijklmnopqrstuvwxyz",
    )

    finding = build_security_finding(indicator)

    assert finding.indicator_type == "GITHUB_TOKEN"
    assert finding.file_path == "config/github.py"
    assert finding.evidence == "ghp_********************"
    assert finding.severity == "high"
    assert finding.confidence == 0.95
    assert finding.requires_review is True


def test_build_security_finding_accepts_custom_metadata():
    indicator = SecurityIndicator(
        indicator_type="AWS_ACCESS_KEY",
        file_path="config/aws.py",
        evidence="AKIA1234567890EXAMPLE",
    )

    finding = build_security_finding(
        indicator,
        severity="critical",
        confidence=0.99,
        requires_review=False,
    )

    assert finding.severity == "critical"
    assert finding.confidence == 0.99
    assert finding.requires_review is False



def test_build_security_finding_uses_classifier():
    indicator = SecurityIndicator(
        indicator_type="AWS_SECRET_KEY",
        file_path="config/aws.py",
        evidence="AWS_********************",
    )

    finding = build_security_finding(indicator)

    assert finding.severity == "critical"
    assert finding.confidence == 0.98
    assert finding.requires_review is True