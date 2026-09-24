from app.services.security_analysis_service import analyze_security


def test_analyze_security_applies_classification():
    files = [
        {
            "path": "config/aws.py",
            "content": "AWS_SECRET_ACCESS_KEY = 'super-secret-value'",
        },
        {
            "path": "config/github.py",
            "content": "token = 'ghp_1234567890abcdefghijklmnopqrstuvwxyz'",
        },
    ]

    findings = analyze_security(files)

    assert len(findings) == 2

    aws_finding = next(
        finding
        for finding in findings
        if finding.indicator_type == "AWS_SECRET_KEY"
    )

    github_finding = next(
        finding
        for finding in findings
        if finding.indicator_type == "GITHUB_TOKEN"
    )

    assert aws_finding.severity == "critical"
    assert aws_finding.confidence == 0.98
    assert aws_finding.requires_review is True

    assert github_finding.severity == "high"
    assert github_finding.confidence == 0.95
    assert github_finding.requires_review is True