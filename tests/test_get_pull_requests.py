from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_pull_requests():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = [
        {
            "number": 123,
            "title": "Add feature",
            "state": "open",
        }
    ]

    client.client.request = Mock(return_value=response)

    result = client.get_pull_requests(
        "microsoft",
        "vscode",
    )

    assert result == [
        {
            "number": 123,
            "title": "Add feature",
            "state": "open",
        }
    ]

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode/pulls",
        params=None,
    )

def test_get_pull_requests_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_pull_requests("", "vscode")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_pull_requests_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_pull_requests("microsoft", "")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )
