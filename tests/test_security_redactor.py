from app.services.security_redactor import redact_secret

from app.models.security_indicator import SecurityIndicator
from app.services.security_redactor import redact_security_indicator


def test_redact_secret():
    secret = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"

    result = redact_secret(secret)

    assert result == "ghp_********************"


def test_redact_short_secret():
    secret = "secret"

    result = redact_secret(secret)

    assert result == "******"


def test_redact_empty_secret():
    result = redact_secret("")

    assert result == ""



def test_redact_security_indicator():
    indicator = SecurityIndicator(
        indicator_type="GITHUB_TOKEN",
        file_path="config/github.py",
        evidence="ghp_1234567890abcdefghijklmnopqrstuvwxyz",
    )

    result = redact_security_indicator(indicator)

    assert result.indicator_type == "GITHUB_TOKEN"
    assert result.file_path == "config/github.py"
    assert result.evidence == "ghp_********************"