from app.models.security_indicator import SecurityIndicator
from app.services.security_classifier import classify_security_indicator


def test_classify_github_token():
    indicator = SecurityIndicator(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_********************",
    )

    classification = classify_security_indicator(indicator)

    assert classification["severity"] == "high"
    assert classification["confidence"] == 0.95
    assert classification["requires_review"] is True


def test_classify_aws_secret_key():
    indicator = SecurityIndicator(
        indicator_type="AWS_SECRET_KEY",
        file_path="config/aws.py",
        evidence="AWS_********************",
    )

    classification = classify_security_indicator(indicator)

    assert classification["severity"] == "critical"
    assert classification["confidence"] == 0.98
    assert classification["requires_review"] is True


def test_classify_unknown_indicator():
    indicator = SecurityIndicator(
        indicator_type="UNKNOWN_SECRET",
        file_path="config/app.py",
        evidence="****",
    )

    classification = classify_security_indicator(indicator)

    assert classification["severity"] == "medium"
    assert classification["confidence"] == 0.70
    assert classification["requires_review"] is True