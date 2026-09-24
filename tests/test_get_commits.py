from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_commits():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = [
        {
            "sha": "abc123",
            "message": "Initial commit",
        }
    ]

    client.client.request = Mock(return_value=response)

    result = client.get_commits(
        "microsoft",
        "vscode",
    )

    assert result == [
        {
            "sha": "abc123",
            "message": "Initial commit",
        }
    ]

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/commits",
        params=None,
    )

def test_get_commits_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_commits("", "vscode")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_commits_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_commits("microsoft", "")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )
