from unittest.mock import Mock

from app.github.client import GitHubClient


def test_get_repository():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = {
        "id": 41881900,
        "full_name": "microsoft/vscode",
        "owner": {
            "login": "microsoft",
        },
        "html_url": "https://github.com/microsoft/vscode",
        "description": "Visual Studio Code",
        "default_branch": "main",
        "visibility": "public",
        "language": "TypeScript",
        "topics": ["editor", "ide"],
        "fork": False,
        "archived": False,
        "stargazers_count": 192751,
        "forks_count": 35000,
        "open_issues_count": 1200,
        "created_at": "2015-01-01T00:00:00Z",
        "updated_at": "2026-09-21T00:00:00Z",
        "pushed_at": "2026-09-21T00:00:00Z",
    }

    client.client.request = Mock(return_value=response)

    result = client.get_repository(
        "microsoft",
        "vscode",
    )

    assert result["full_name"] == "microsoft/vscode"
    assert result["stargazers_count"] == 192751

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode",
        params=None,
    )