from unittest.mock import Mock

from app.github.client import GitHubClient
from app.github.exceptions import GitHubAPIError


def test_github_api_error():
    client = GitHubClient()

    response = Mock(status_code=404)
    response.headers = {}

    client.client.request = Mock(return_value=response)

    try:
        client.get_repository(
            "microsoft",
            "this-repository-does-not-exist-123456789",
        )
    except GitHubAPIError as error:
        assert type(error).__name__ == "GitHubAPIError"
        assert error.status_code == 404
        assert str(error) == "GitHub API request failed with status 404"
    else:
        raise AssertionError("Expected GitHubAPIError was not raised")
