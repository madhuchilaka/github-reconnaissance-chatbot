from app.models.security_indicator import SecurityIndicator
from app.services.security_relationship_service import (
    build_security_relationship,
)


def test_build_security_relationship():
    indicator = SecurityIndicator(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_********************",
    )

    relationship = build_security_relationship(
        indicator=indicator,
        context="token used in GitHub client configuration",
        related_files=[
            "config/settings.py",
            "app/github/client.py",
        ],
        confidence=0.90,
    )

    assert relationship.indicator_type == "GITHUB_TOKEN"
    assert relationship.file_path == "config/github.py"
    assert relationship.context == (
        "token used in GitHub client configuration"
    )
    assert relationship.related_files == (
        "config/settings.py",
        "app/github/client.py",
    )
    assert relationship.confidence == 0.90


def test_build_security_relationship_with_no_related_files():
    indicator = SecurityIndicator(
        indicator_type="AWS_SECRET_KEY",
        file_path="config/aws.py",
        evidence="AWS_********************",
    )

    relationship = build_security_relationship(
        indicator=indicator,
        context="AWS configuration",
        related_files=[],
        confidence=0.80,
    )

    assert relationship.related_files == ()


def test_build_security_relationship_does_not_expose_indicator_evidence():
    indicator = SecurityIndicator(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_********************",
    )

    relationship = build_security_relationship(
        indicator=indicator,
        context="GitHub authentication configuration",
        related_files=["app/github/client.py"],
        confidence=0.90,
    )

    assert relationship.context == "GitHub authentication configuration"
    assert "ghp_" not in relationship.context
    assert relationship.related_files == ("app/github/client.py",)