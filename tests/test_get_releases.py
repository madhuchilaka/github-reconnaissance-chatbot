from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_releases():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = [
        {
            "tag_name": "v1.0.0",
            "name": "Initial Release",
            "draft": False,
            "prerelease": False,
        }
    ]

    client.client.request = Mock(return_value=response)

    result = client.get_releases(
        "microsoft",
        "vscode",
    )

    assert result == [
        {
            "tag_name": "v1.0.0",
            "name": "Initial Release",
            "draft": False,
            "prerelease": False,
        }
    ]

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/releases",
        params=None,
    )

def test_get_releases_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_releases("", "vscode")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_releases_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_releases("microsoft", "")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )
