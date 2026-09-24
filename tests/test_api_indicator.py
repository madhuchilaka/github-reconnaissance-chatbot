from app.models.api_indicator import ApiIndicator


def test_api_indicator_fields():
    indicator = ApiIndicator(
        url="https://api.example.com/users",
        method="GET",
        evidence=["src/client.py"],
    )

    assert indicator.url == "https://api.example.com/users"
    assert indicator.method == "GET"
    assert indicator.evidence == ["src/client.py"]


def test_api_indicator_is_immutable():
    indicator = ApiIndicator(
        url="https://api.example.com/users",
        method="GET",
        evidence=["src/client.py"],
    )

    try:
        indicator.url = "https://other.example.com"
        assert False
    except AttributeError:
        pass
