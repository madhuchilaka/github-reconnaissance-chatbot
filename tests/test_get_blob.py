from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_blob():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = {
        "sha": "def456",
        "size": 12,
        "content": "SGVsbG8gV29ybGQ=",
        "encoding": "base64",
    }

    client.client.request = Mock(return_value=response)

    result = client.get_blob(
        "microsoft",
        "vscode",
        "def456",
    )

    assert result == {
        "sha": "def456",
        "size": 12,
        "content": "SGVsbG8gV29ybGQ=",
        "encoding": "base64",
    }

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/git/blobs/def456",
        params=None,
    )


def test_get_blob_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_blob("", "vscode", "def456")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_blob_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_blob("microsoft", "", "def456")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_blob_rejects_empty_sha():
    client = GitHubClient()

    try:
        client.get_blob("microsoft", "vscode", "")
    except ValueError as error:
        assert str(error) == "Blob SHA cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )