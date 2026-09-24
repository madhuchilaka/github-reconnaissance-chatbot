from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_file():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = {
        "name": "README.md",
        "path": "README.md",
        "type": "file",
        "content": "SGVsbG8gV29ybGQ=",
        "encoding": "base64",
    }

    client.client.request = Mock(return_value=response)

    result = client.get_file(
        "microsoft",
        "vscode",
        "README.md",
    )

    assert result == {
        "name": "README.md",
        "path": "README.md",
        "type": "file",
        "content": "SGVsbG8gV29ybGQ=",
        "encoding": "base64",
    }

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/contents/README.md",
        params=None,
    )

def test_get_file_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_file("", "vscode", "README.md")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_file_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_file("microsoft", "", "README.md")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_file_rejects_empty_path():
    client = GitHubClient()

    try:
        client.get_file("microsoft", "vscode", "")
    except ValueError as error:
        assert str(error) == "File path cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )
