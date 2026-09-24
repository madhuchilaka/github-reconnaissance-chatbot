from app.models.security_indicator import SecurityIndicator
from app.services.security_finding_service import build_security_findings


def test_build_security_findings_for_multiple_indicators():
    indicators = [
        SecurityIndicator(
            indicator_type="GITHUB_TOKEN",
            file_path="config/github.py",
            evidence="ghp_1234567890abcdefghijklmnopqrstuvwxyz",
        ),
        SecurityIndicator(
            indicator_type="AWS_ACCESS_KEY",
            file_path="config/aws.py",
            evidence="AKIA1234567890EXAMPLE",
        ),
    ]

    findings = build_security_findings(indicators)

    assert len(findings) == 2

    assert findings[0].indicator_type == "GITHUB_TOKEN"
    assert findings[0].file_path == "config/github.py"
    assert findings[0].evidence == "ghp_********************"

    assert findings[1].indicator_type == "AWS_ACCESS_KEY"
    assert findings[1].file_path == "config/aws.py"
    assert findings[1].evidence == "AKIA********************"


def test_build_security_findings_with_empty_input():
    findings = build_security_findings([])

    assert findings == []



def test_build_security_findings_uses_classification():
    indicators = [
        SecurityIndicator(
            indicator_type="AWS_SECRET_KEY",
            file_path="config/aws.py",
            evidence="AWS_********************",
        ),
        SecurityIndicator(
            indicator_type="UNKNOWN_SECRET",
            file_path="config/app.py",
            evidence="****",
        ),
    ]

    findings = build_security_findings(indicators)

    assert findings[0].severity == "critical"
    assert findings[0].confidence == 0.98
    assert findings[0].requires_review is True

    assert findings[1].severity == "medium"
    assert findings[1].confidence == 0.70
    assert findings[1].requires_review is True