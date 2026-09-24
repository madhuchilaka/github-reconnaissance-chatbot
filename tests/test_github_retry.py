import httpx

from unittest.mock import Mock, patch

from app.github.client import GitHubClient
from app.github.exceptions import GitHubAPIError


def test_retry_on_server_error():
    client = GitHubClient()

    responses = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=200),
    ]

    for response in responses:
        response.headers = {}

    client.client.request = Mock(side_effect=responses)
    client._get_retry_delay = Mock(return_value=0)

    result = client.get_repository("microsoft", "vscode")

    assert result == responses[2].json.return_value
    assert client.client.request.call_count == 3
    assert client._get_retry_delay.call_count == 2


def test_no_retry_on_not_found():
    client = GitHubClient()

    response = Mock(status_code=404)
    response.headers = {}

    client.client.request = Mock(return_value=response)

    try:
        client.get_repository("microsoft", "does-not-exist")
    except GitHubAPIError as error:
        assert error.status_code == 404

    assert client.client.request.call_count == 1

def test_stops_after_max_retries():
    client = GitHubClient()

    response = Mock(status_code=500)
    response.headers = {}

    client.client.request = Mock(return_value=response)
    client._get_retry_delay = Mock(return_value=0)

    try:
        client.get_repository("microsoft", "vscode")
    except GitHubAPIError as error:
        assert error.status_code == 500

    assert client.client.request.call_count == 4
    assert client._get_retry_delay.call_count == 3


def test_preserves_retry_after():
    client = GitHubClient()

    response = Mock(status_code=429)
    response.headers = {"Retry-After": "30"}

    client.client.request = Mock(return_value=response)
    client._get_retry_delay = Mock(return_value=0)

    with patch("app.github.client.time.sleep") as mock_sleep:
        try:
            client.get_repository("microsoft", "vscode")
        except GitHubAPIError as error:
            assert error.status_code == 429
            assert error.retry_after == 30.0
            assert mock_sleep.call_count == 3
            mock_sleep.assert_called_with(30.0)


def test_get_paginated():
    client = GitHubClient()

    page_1 = Mock(status_code=200)
    page_1.json.return_value = [
        {"id": index} for index in range(100)
    ]

    page_2 = Mock(status_code=200)
    page_2.json.return_value = [{"id": 100}]

    client.client.request = Mock(
        side_effect=[page_1, page_2]
    )

    result = client.get_paginated(
        "/repos/microsoft/vscode/issues",
        max_pages=10,
    )

    assert len(result) == 101
    assert result[0] == {"id": 0}
    assert result[-1] == {"id": 100}

    assert client.client.request.call_count == 2


def test_get_paginated_respects_max_pages():
    client = GitHubClient()

    page_1 = Mock(status_code=200)
    page_1.json.return_value = [
        {"id": index} for index in range(100)
    ]

    page_2 = Mock(status_code=200)
    page_2.json.return_value = [
        {"id": index} for index in range(100, 200)
    ]

    page_3 = Mock(status_code=200)
    page_3.json.return_value = [
        {"id": 200}
    ]

    client.client.request = Mock(
        side_effect=[page_1, page_2, page_3]
    )

    result = client.get_paginated(
        "/repos/microsoft/vscode/issues",
        max_pages=2,
    )

    assert len(result) == 200
    assert result[-1] == {"id": 199}
    assert client.client.request.call_count == 2


def test_get_paginated_raises_on_api_error():
    client = GitHubClient()

    page_1 = Mock(status_code=200)
    page_1.json.return_value = [
        {"id": index} for index in range(100)
    ]

    page_2 = Mock(status_code=404)
    page_2.headers = {}

    client.client.request = Mock(
        side_effect=[page_1, page_2]
    )

    try:
        client.get_paginated(
            "/repos/microsoft/vscode/issues",
            max_pages=10,
        )
    except GitHubAPIError as error:
        assert error.status_code == 404

    assert client.client.request.call_count == 2


def test_github_client_sets_required_headers():
    client = GitHubClient()

    assert client.client.headers["Accept"] == "application/vnd.github+json"


def test_github_client_uses_token_when_configured(monkeypatch):
    monkeypatch.setattr(
        "app.github.client.GITHUB_TOKEN",
        "test-token",
    )

    client = GitHubClient()

    assert (
        client.client.headers["Authorization"]
        == "Bearer test-token"
    )


def test_request_exposes_rate_limit_headers():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {
        "X-RateLimit-Limit": "5000",
        "X-RateLimit-Remaining": "4999",
        "X-RateLimit-Reset": "1770000000",
    }

    client.client.request = Mock(return_value=response)

    result = client._request(
        "GET",
        "/repos/microsoft/vscode",
    )

    assert result.headers["X-RateLimit-Limit"] == "5000"
    assert result.headers["X-RateLimit-Remaining"] == "4999"
    assert result.headers["X-RateLimit-Reset"] == "1770000000"


def test_request_preserves_pagination_link_header():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {
        "Link": (
            '<https://api.github.com/repos/microsoft/vscode/issues?page=2>; '
            'rel="next", '
            '<https://api.github.com/repos/microsoft/vscode/issues?page=10>; '
            'rel="last"'
        )
    }

    client.client.request = Mock(return_value=response)

    result = client._request(
        "GET",
        "/repos/microsoft/vscode/issues",
    )

    assert result.headers["Link"] == response.headers["Link"] 


def test_request_handles_timeout():
    client = GitHubClient()

    client.client.request = Mock(
        side_effect=httpx.TimeoutException("Request timed out")
    )

    try:
        client._request(
            "GET",
            "/repos/microsoft/vscode",
        )
    except httpx.TimeoutException as error:
        assert str(error) == "Request timed out"
    else:
        raise AssertionError(
            "Expected httpx.TimeoutException was not raised"
        )


def test_get_repository_rejects_empty_owner():
    client = GitHubClient()

    try:
        client.get_repository("", "vscode")
    except ValueError as error:
        assert str(error) == "Repository owner cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_get_repository_rejects_empty_repo():
    client = GitHubClient()

    try:
        client.get_repository("microsoft", "")
    except ValueError as error:
        assert str(error) == "Repository name cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_github_api_error_does_not_expose_token():
    client = GitHubClient()

    response = Mock(status_code=404)
    response.headers = {}

    client.client.request = Mock(return_value=response)

    secret_token = "ghp_TEST_SECRET_TOKEN"

    try:
        client._request(
            "GET",
            "/repos/microsoft/vscode",
        )
    except GitHubAPIError as error:
        assert secret_token not in str(error)
        assert "Authorization" not in str(error)
        assert str(error) == (
            "GitHub API request failed with status 404"
        )
    else:
        raise AssertionError(
            "Expected GitHubAPIError was not raised"
        )


def test_github_client_can_be_closed():
    client = GitHubClient()

    client.client.close = Mock()

    client.close()

    client.client.close.assert_called_once()


def test_get_repository_end_to_end():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = {
        "full_name": "microsoft/vscode",
        "private": False,
        "stargazers_count": 192000,
    }

    client.client.request = Mock(return_value=response)

    result = client.get_repository(
        "microsoft",
        "vscode",
    )

    assert result == {
        "full_name": "microsoft/vscode",
        "private": False,
        "stargazers_count": 192000,
    }

    client.client.request.assert_called_once_with(
        "GET",
        "/repos/microsoft/vscode",
        params=None,
    )


def test_search_repositories():
    client = GitHubClient()

    response = Mock(status_code=200)
    response.headers = {}
    response.json.return_value = {
        "total_count": 2,
        "incomplete_results": False,
        "items": [
            {
                "full_name": "microsoft/vscode",
            },
            {
                "full_name": "microsoft/TypeScript",
            },
        ],
    }

    client.client.request = Mock(return_value=response)

    result = client.search_repositories(
        "microsoft",
        page=2,
        per_page=50,
    )

    assert result == {
        "total_count": 2,
        "incomplete_results": False,
        "items": [
            {
                "full_name": "microsoft/vscode",
            },
            {
                "full_name": "microsoft/TypeScript",
            },
        ],
    }

    client.client.request.assert_called_once_with(
        "GET",
        "/search/repositories",
        params={
            "q": "microsoft",
            "page": 2,
            "per_page": 50,
        },
    )


def test_search_repositories_rejects_empty_query():
    client = GitHubClient()

    try:
        client.search_repositories("")
    except ValueError as error:
        assert str(error) == "Repository search query cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_search_repositories_rejects_whitespace_query():
    client = GitHubClient()

    try:
        client.search_repositories("   ")
    except ValueError as error:
        assert str(error) == "Repository search query cannot be empty"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )