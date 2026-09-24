from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_branches():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = [
        {
            "name": "main",
            "protected": True,
        },
        {
            "name": "develop",
            "protected": False,
        },
    ]

    client.client.request = Mock(return_value=response)

    result = client.get_branches(
        "microsoft",
        "vscode",
    )

    assert result == [
        {
            "name": "main",
            "protected": True,
        },
        {
            "name": "develop",
            "protected": False,
        },
    ]

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/branches",
        params=None,
    )

def test_get_branches_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_branches("", "vscode")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_branches_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_branches("microsoft", "")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )
