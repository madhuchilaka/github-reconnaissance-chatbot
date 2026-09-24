from app.models.domain_indicator import DomainIndicator


def test_domain_indicator():
    indicator = DomainIndicator(
        domain="api.example.com",
        evidence=["config/settings.py"],
    )

    assert indicator.domain == "api.example.com"
    assert indicator.evidence == ["config/settings.py"]


def test_domain_indicator_is_immutable():
    indicator = DomainIndicator(
        domain="api.example.com",
        evidence=["config/settings.py"],
    )

    try:
        indicator.domain = "other.example.com"
        assert False
    except AttributeError:
        pass