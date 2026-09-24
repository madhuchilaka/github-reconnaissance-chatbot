from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_contributors():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = [
        {
            "login": "octocat",
            "contributions": 42,
        },
        {
            "login": "developer",
            "contributions": 18,
        },
    ]

    client.client.request = Mock(return_value=response)

    result = client.get_contributors(
        "microsoft",
        "vscode",
    )

    assert result == [
        {
            "login": "octocat",
            "contributions": 42,
        },
        {
            "login": "developer",
            "contributions": 18,
        },
    ]

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/contributors",
        params=None,
    )

def test_get_contributors_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_contributors("", "vscode")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_contributors_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_contributors("microsoft", "")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )
