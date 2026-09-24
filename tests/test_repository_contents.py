from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_repository_contents():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = [
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
        }
    ]

    client.client.request = Mock(return_value=response)

    result = client.get_repository_contents(
        "microsoft",
        "vscode",
    )

    assert result == [
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
        }
    ]

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/contents/",
        params=None,
    )

def test_get_repository_contents_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_repository_contents("", "vscode")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_repository_contents_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_repository_contents("microsoft", "")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )
