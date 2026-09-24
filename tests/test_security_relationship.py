from app.models.security_relationship import SecurityRelationship


def test_security_relationship_fields():
    relationship = SecurityRelationship(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        context="token used in GitHub client configuration",
        related_files=("config/settings.py", "app/github/client.py"),
        confidence=0.90,
    )

    assert relationship.indicator_type == "GITHUB_TOKEN"
    assert relationship.file_path == "config/github.py"
    assert relationship.context == "token used in GitHub client configuration"
    assert relationship.related_files == (
        "config/settings.py",
        "app/github/client.py",
    )
    assert relationship.confidence == 0.90


def test_security_relationship_is_immutable():
    relationship = SecurityRelationship(
        indicator_type="AWS_SECRET_KEY",
        file_path="config/aws.py",
        context="AWS configuration",
        related_files=("app/aws/client.py",),
        confidence=0.85,
    )

    try:
        relationship.confidence = 0.50
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "SecurityRelationship should be immutable"
        )