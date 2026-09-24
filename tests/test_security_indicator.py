from app.models.security_indicator import SecurityIndicator


def test_security_indicator_fields():
    indicator = SecurityIndicator(
        indicator_type="AWS_ACCESS_KEY",
        file_path="config/settings.py",
        evidence="AWS_ACCESS_KEY_ID",
    )

    assert indicator.indicator_type == "AWS_ACCESS_KEY"
    assert indicator.file_path == "config/settings.py"
    assert indicator.evidence == "AWS_ACCESS_KEY_ID"


def test_security_indicator_is_immutable():
    indicator = SecurityIndicator(
        indicator_type="AWS_ACCESS_KEY",
        file_path="config/settings.py",
        evidence="AWS_ACCESS_KEY_ID",
    )

    try:
        indicator.file_path = "other.py"
        assert False
    except AttributeError:
        pass
