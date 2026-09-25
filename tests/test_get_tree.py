from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_tree():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = {
        "sha": "abc123",
        "tree": [
            {
                "path": "README.md",
                "mode": "100644",
                "type": "blob",
                "sha": "def456",
                "size": 100,
            }
        ],
        "truncated": False,
    }

    client.client.request = Mock(return_value=response)

    result = client.get_tree(
        "microsoft",
        "vscode",
        "main",
    )

    assert result == {
        "sha": "abc123",
        "tree": [
            {
                "path": "README.md",
                "mode": "100644",
                "type": "blob",
                "sha": "def456",
                "size": 100,
            }
        ],
        "truncated": False,
    }

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/git/trees/main",
        params={"recursive": "1"},
    )


def test_get_tree_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_tree("", "vscode", "main")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_tree_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_tree("microsoft", "", "main")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_tree_rejects_empty_tree_sha():
    client = GitHubClient()

    try:
        client.get_tree("microsoft", "vscode", "")
    except ValueError as error:
        assert str(error) == "Tree SHA cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )