from app.models.security_finding import SecurityFinding
from app.services.security_relationship_analysis_service import (
    analyze_security_relationship,
    analyze_security_relationships,
)



def test_analyze_security_relationship():
    finding = SecurityFinding(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
    )

    relationship = analyze_security_relationship(
        finding=finding,
        context="GitHub authentication configuration",
        related_files=["app/github/client.py"],
    )

    assert relationship.indicator_type == "GITHUB_TOKEN"
    assert relationship.file_path == "config/github.py"
    assert relationship.context == "GitHub authentication configuration"
    assert relationship.related_files == ("app/github/client.py",)
    assert relationship.confidence == 0.95


def test_analyze_security_relationship_preserves_review_context():
    finding = SecurityFinding(
        indicator_type="AWS_SECRET_KEY",
        file_path="config/aws.py",
        evidence="AWS_********************",
        severity="critical",
        confidence=0.98,
        requires_review=True,
    )

    relationship = analyze_security_relationship(
        finding=finding,
        context="AWS SDK configuration",
        related_files=[],
    )

    assert relationship.indicator_type == "AWS_SECRET_KEY"
    assert relationship.confidence == 0.98
    assert relationship.related_files == ()


def test_analyze_security_relationships():
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

    relationships = analyze_security_relationships(
        findings=findings,
        context_by_file={
            "config/github.py": "GitHub authentication configuration",
            "config/aws.py": "AWS SDK configuration",
        },
        related_files_by_file={
            "config/github.py": ["app/github/client.py"],
            "config/aws.py": ["app/aws/client.py"],
        },
    )

    assert len(relationships) == 2

    assert relationships[0].indicator_type == "GITHUB_TOKEN"
    assert relationships[0].confidence == 0.95
    assert relationships[0].related_files == (
        "app/github/client.py",
    )

    assert relationships[1].indicator_type == "AWS_SECRET_KEY"
    assert relationships[1].confidence == 0.98
    assert relationships[1].related_files == (
        "app/aws/client.py",
    )