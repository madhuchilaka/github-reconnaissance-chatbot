from unittest.mock import Mock

from app.models.repository import RepositoryCandidate
from app.services.repository_service import RepositoryService
from app.models.repository_metadata import RepositoryMetadata
from app.tools.definitions import SEARCH_REPOSITORIES_TOOL
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.dispatcher import ToolDispatcher
import pytest
from app.tools.validation import (
    validate_get_branches_arguments,
    validate_get_commits_arguments,
    validate_get_contributors_arguments,
    validate_get_file_arguments,
    validate_get_pull_requests_arguments,
    validate_get_releases_arguments,
    validate_get_repository_arguments,
    validate_get_repository_contents_arguments,
    validate_search_code_arguments,
    validate_search_repositories_arguments,
)
from app.tools.results import ToolResult
from app.tools.errors import ToolExecutionError



def test_repository_candidates_from_search_result():
    search_result = {
        "total_count": 2,
        "incomplete_results": False,
        "items": [
            {
                "full_name": "microsoft/vscode",
                "owner": {
                    "login": "microsoft",
                },
                "html_url": "https://github.com/microsoft/vscode",
                "description": "Visual Studio Code",
                "fork": False,
                "default_branch": "main",
            },
            {
                "full_name": "microsoft/TypeScript",
                "owner": {
                    "login": "microsoft",
                },
                "html_url": "https://github.com/microsoft/TypeScript",
                "description": "TypeScript",
                "fork": False,
                "default_branch": "main",
            },
        ],
    }

    repositories = RepositoryService.to_candidates(search_result)

    assert repositories == [
        RepositoryCandidate(
            full_name="microsoft/vscode",
            owner_login="microsoft",
            html_url="https://github.com/microsoft/vscode",
            description="Visual Studio Code",
            fork=False,
            default_branch="main",
        ),
        RepositoryCandidate(
            full_name="microsoft/TypeScript",
            owner_login="microsoft",
            html_url="https://github.com/microsoft/TypeScript",
            description="TypeScript",
            fork=False,
            default_branch="main",
        ),
    ]

def test_repository_candidates_from_empty_search_result():
    search_result = {
        "total_count": 0,
        "incomplete_results": False,
        "items": [],
    }

    repositories = RepositoryService.to_candidates(search_result)

    assert repositories == []



def test_search_repositories_returns_candidates():
    client = Mock()

    client.search_repositories.return_value = {
        "total_count": 1,
        "incomplete_results": False,
        "items": [
            {
                "full_name": "microsoft/vscode",
                "owner": {
                    "login": "microsoft",
                },
                "html_url": "https://github.com/microsoft/vscode",
                "description": "Visual Studio Code",
                "fork": False,
                "default_branch": "main",
            }
        ],
    }

    repositories = RepositoryService.search_repositories(
        client,
        "microsoft",
    )

    assert repositories == [
        RepositoryCandidate(
            full_name="microsoft/vscode",
            owner_login="microsoft",
            html_url="https://github.com/microsoft/vscode",
            description="Visual Studio Code",
            fork=False,
            default_branch="main",
        )
    ]

    client.search_repositories.assert_called_once_with("microsoft")



def test_get_repository_metadata():
    client = Mock()

    client.get_repository.return_value = {
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

    repository = RepositoryService.get_repository_metadata(
        client,
        "microsoft",
        "vscode",
    )

    assert repository == RepositoryMetadata(
        id=41881900,
        full_name="microsoft/vscode",
        owner_login="microsoft",
        html_url="https://github.com/microsoft/vscode",
        description="Visual Studio Code",
        default_branch="main",
        visibility="public",
        language="TypeScript",
        topics=["editor", "ide"],
        fork=False,
        archived=False,
        stargazers_count=192751,
        forks_count=35000,
        open_issues_count=1200,
        created_at="2015-01-01T00:00:00Z",
        updated_at="2026-09-21T00:00:00Z",
        pushed_at="2026-09-21T00:00:00Z",
    )

    client.get_repository.assert_called_once_with(
        "microsoft",
        "vscode",
    )


def test_search_repositories_tool_definition():
    assert SEARCH_REPOSITORIES_TOOL["name"] == "search_repositories"
    assert SEARCH_REPOSITORIES_TOOL["description"] == "Search public GitHub repositories."

    parameters = SEARCH_REPOSITORIES_TOOL["parameters"]

    assert parameters["type"] == "object"
    assert "query" in parameters["properties"]
    assert "page" in parameters["properties"]
    assert "per_page" in parameters["properties"]

    assert parameters["required"] == ["query"]



def test_tool_executor_search_repositories():
    client = Mock()
    client.search_repositories.return_value = {
        "total_count": 1,
        "items": [
            {
                "full_name": "microsoft/vscode",
            }
        ],
    }

    executor = ToolExecutor(client)

    result = executor.search_repositories(
        query="microsoft",
        page=2,
        per_page=50,
    )

    assert result["total_count"] == 1
    assert result["items"][0]["full_name"] == "microsoft/vscode"

    client.search_repositories.assert_called_once_with(
        query="microsoft",
        page=2,
        per_page=50,
    ) 


def test_tool_registry():
    registry = ToolRegistry()

    search_tool = registry.get("search_repositories")
    repository_tool = registry.get("get_repository")
    contents_tool = registry.get("get_repository_contents")
    code_tool = registry.get("search_code")
    file_tool = registry.get("get_file")
    commits_tool = registry.get("get_commits")
    branches_tool = registry.get("get_branches")
    pull_requests_tool = registry.get("get_pull_requests")
    contributors_tool = registry.get("get_contributors")
    releases_tool = registry.get("get_releases")

    assert search_tool["name"] == "search_repositories"
    assert repository_tool["name"] == "get_repository"
    assert contents_tool["name"] == "get_repository_contents"
    assert code_tool["name"] == "search_code"
    assert file_tool["name"] == "get_file"
    assert commits_tool["name"] == "get_commits"
    assert branches_tool["name"] == "get_branches"
    assert pull_requests_tool["name"] == "get_pull_requests"
    assert contributors_tool["name"] == "get_contributors"
    assert releases_tool["name"] == "get_releases"

    tools = registry.all()

    assert len(tools) == 10

    tool_names = {tool["name"] for tool in tools}

    assert tool_names == {
        "search_repositories",
        "get_repository",
        "get_repository_contents",
        "search_code",
        "get_file",
        "get_commits",
        "get_branches",
        "get_pull_requests",
        "get_contributors",
        "get_releases",
    }

def test_tool_dispatcher():
    executor = Mock()
    executor.search_repositories.return_value = {
        "total_count": 1,
        "items": [
            {
                "full_name": "microsoft/vscode",
            }
        ],
    }

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "search_repositories",
        {
            "query": "microsoft",
            "page": 1,
            "per_page": 10,
        },
    )

    assert result.tool_name == "search_repositories"
    assert result.success is True
    assert result.data["total_count"] == 1
    assert result.data["items"][0]["full_name"] == "microsoft/vscode"
    assert result.error is None

    executor.search_repositories.assert_called_once_with(
        query="microsoft",
        page=1,
        per_page=10,
    )



def test_tool_dispatcher_rejects_unknown_tool():
    executor = Mock()
    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    with pytest.raises(ValueError, match="Unknown tool"):
        dispatcher.dispatch(
            "unknown_tool",
            {},
        )


def test_validate_search_repositories_arguments_accepts_valid_arguments():
    validate_search_repositories_arguments(
        {
            "query": "machine learning",
            "page": 2,
            "per_page": 50,
        }
    )


def test_validate_search_repositories_arguments_rejects_invalid_query():
    with pytest.raises(ValueError, match="Repository search query cannot be empty"):
        validate_search_repositories_arguments(
            {
                "query": "",
            }
        )


def test_validate_search_repositories_arguments_rejects_invalid_page():
    with pytest.raises(ValueError, match="Page must be a positive integer"):
        validate_search_repositories_arguments(
            {
                "query": "machine learning",
                "page": 0,
            }
        )


def test_validate_search_repositories_arguments_rejects_invalid_per_page():
    with pytest.raises(
        ValueError,
        match="per_page must be an integer between 1 and 100",
    ):
        validate_search_repositories_arguments(
            {
                "query": "machine learning",
                "per_page": 101,
            }
        )


def test_validate_search_code_arguments_accepts_valid_arguments():
    validate_search_code_arguments(
        {
            "query": "password",
            "page": 2,
            "per_page": 50,
        }
    )


def test_validate_search_code_arguments_rejects_invalid_query():
    with pytest.raises(
        ValueError,
        match="Code search query cannot be empty",
    ):
        validate_search_code_arguments(
            {
                "query": "",
            }
        )


def test_validate_search_code_arguments_rejects_invalid_page():
    with pytest.raises(
        ValueError,
        match="Page must be a positive integer",
    ):
        validate_search_code_arguments(
            {
                "query": "password",
                "page": 0,
            }
        )


def test_validate_search_code_arguments_rejects_invalid_per_page():
    with pytest.raises(
        ValueError,
        match="per_page must be an integer between 1 and 100",
    ):
        validate_search_code_arguments(
            {
                "query": "password",
                "per_page": 101,
            }
        )



def test_tool_dispatcher_validates_search_arguments():
    executor = Mock()
    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    with pytest.raises(
        ValueError,
        match="per_page must be an integer between 1 and 100",
    ):
        dispatcher.dispatch(
            "search_repositories",
            {
                "query": "machine learning",
                "page": 1,
                "per_page": 101,
            },
        )

    executor.search_repositories.assert_not_called()


def test_tool_result():
    result = ToolResult(
        tool_name="search_repositories",
        success=True,
        data={
            "total_count": 1,
            "items": [
                {
                    "full_name": "microsoft/vscode",
                }
            ],
        },
    )

    assert result.tool_name == "search_repositories"
    assert result.success is True
    assert result.data["total_count"] == 1
    assert result.error is None



def test_tool_result_success_result():
    result = ToolResult.success_result(
        "search_repositories",
        {
            "total_count": 1,
            "items": [
                {
                    "full_name": "microsoft/vscode",
                }
            ],
        },
    )

    assert result.tool_name == "search_repositories"
    assert result.success is True
    assert result.data["total_count"] == 1
    assert result.error is None



def test_tool_result_error_result():
    result = ToolResult.error_result(
        "search_repositories",
        "Repository search failed",
    )

    assert result.tool_name == "search_repositories"
    assert result.success is False
    assert result.data is None
    assert result.error == "Repository search failed"



def test_tool_execution_error():
    error = ToolExecutionError("Tool execution failed")

    assert str(error) == "Tool execution failed"



def test_tool_executor_converts_execution_errors():
    client = Mock()
    client.search_repositories.side_effect = RuntimeError("GitHub unavailable")

    executor = ToolExecutor(client)

    with pytest.raises(
        ToolExecutionError,
        match="Repository search failed: GitHub unavailable",
    ):
        executor.search_repositories(
            query="microsoft",
            page=1,
            per_page=10,
        )



def test_tool_dispatcher_returns_error_result_on_execution_failure():
    executor = Mock()
    executor.search_repositories.side_effect = ToolExecutionError(
        "Repository search failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "search_repositories",
        {
            "query": "microsoft",
            "page": 1,
            "per_page": 10,
        },
    )

    assert result.tool_name == "search_repositories"
    assert result.success is False
    assert result.data is None
    assert result.error == "Repository search failed: GitHub unavailable"



def test_tool_dispatcher_rejects_registered_but_unimplemented_tool():
    executor = Mock()
    registry = ToolRegistry()

    registry._tools["future_tool"] = {
        "name": "future_tool",
        "description": "A future tool",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }

    dispatcher = ToolDispatcher(
        executor,
        registry,
    )

    with pytest.raises(
        ValueError,
        match="Tool is registered but not implemented: future_tool",
    ):
        dispatcher.dispatch(
            "future_tool",
            {},
        )


def test_tool_executor_get_repository():
    client = Mock()
    client.get_repository.return_value = {
        "full_name": "microsoft/vscode",
        "stargazers_count": 192000,
    }

    executor = ToolExecutor(client)

    result = executor.get_repository(
        owner="microsoft",
        repo="vscode",
    )

    assert result["full_name"] == "microsoft/vscode"
    assert result["stargazers_count"] == 192000

    client.get_repository.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
    )   



def test_validate_get_repository_arguments_accepts_valid_arguments():
    validate_get_repository_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
        }
    )


def test_validate_get_repository_arguments_rejects_empty_owner():
    with pytest.raises(
        ValueError,
        match="Repository owner cannot be empty",
    ):
        validate_get_repository_arguments(
            {
                "owner": "",
                "repo": "vscode",
            }
        )


def test_validate_get_repository_arguments_rejects_empty_repo():
    with pytest.raises(
        ValueError,
        match="Repository name cannot be empty",
    ):
        validate_get_repository_arguments(
            {
                "owner": "microsoft",
                "repo": "",
            }
        )



def test_tool_dispatcher_get_repository():
    executor = Mock()
    executor.get_repository.return_value = {
        "full_name": "microsoft/vscode",
        "stargazers_count": 192000,
    }

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_repository",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_repository"
    assert result.success is True
    assert result.data["full_name"] == "microsoft/vscode"
    assert result.data["stargazers_count"] == 192000
    assert result.error is None

    executor.get_repository.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
    )


def test_tool_dispatcher_get_repository_returns_error_result_on_failure():
    executor = Mock()
    executor.get_repository.side_effect = ToolExecutionError(
        "Repository lookup failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_repository",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_repository"
    assert result.success is False
    assert result.data is None
    assert result.error == "Repository lookup failed: GitHub unavailable"




def test_tool_executor_get_repository_contents():
    client = Mock()
    client.get_repository_contents.return_value = [
        {
            "name": "README.md",
            "type": "file",
        },
        {
            "name": "app",
            "type": "dir",
        },
    ]

    executor = ToolExecutor(client)

    result = executor.get_repository_contents(
        owner="microsoft",
        repo="vscode",
        path="",
    )

    assert result[0]["name"] == "README.md"
    assert result[0]["type"] == "file"
    assert result[1]["name"] == "app"
    assert result[1]["type"] == "dir"

    client.get_repository_contents.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
        path="",
    )


def test_validate_get_repository_contents_arguments_accepts_valid_arguments():
    validate_get_repository_contents_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
            "path": "src",
        }
    )


def test_validate_get_repository_contents_arguments_accepts_empty_path():
    validate_get_repository_contents_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
            "path": "",
        }
    )


def test_validate_get_repository_contents_arguments_rejects_empty_owner():
    with pytest.raises(
        ValueError,
        match="Repository owner cannot be empty",
    ):
        validate_get_repository_contents_arguments(
            {
                "owner": "",
                "repo": "vscode",
                "path": "",
            }
        )


def test_validate_get_repository_contents_arguments_rejects_empty_repo():
    with pytest.raises(
        ValueError,
        match="Repository name cannot be empty",
    ):
        validate_get_repository_contents_arguments(
            {
                "owner": "microsoft",
                "repo": "",
                "path": "",
            }
        )


def test_validate_get_repository_contents_arguments_rejects_non_string_path():
    with pytest.raises(
        ValueError,
        match="Repository path must be a string",
    ):
        validate_get_repository_contents_arguments(
            {
                "owner": "microsoft",
                "repo": "vscode",
                "path": 123,
            }
        )


def test_tool_dispatcher_get_repository_contents():
    executor = Mock()
    executor.get_repository_contents.return_value = [
        {
            "name": "README.md",
            "type": "file",
        },
        {
            "name": "src",
            "type": "dir",
        },
    ]

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_repository_contents",
        {
            "owner": "microsoft",
            "repo": "vscode",
            "path": "",
        },
    )

    assert result.tool_name == "get_repository_contents"
    assert result.success is True
    assert result.data[0]["name"] == "README.md"
    assert result.data[1]["name"] == "src"
    assert result.error is None

    executor.get_repository_contents.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
        path="",
    )



def test_tool_dispatcher_get_repository_contents_returns_error_result_on_failure():
    executor = Mock()
    executor.get_repository_contents.side_effect = ToolExecutionError(
        "Repository contents lookup failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_repository_contents",
        {
            "owner": "microsoft",
            "repo": "vscode",
            "path": "",
        },
    )

    assert result.tool_name == "get_repository_contents"
    assert result.success is False
    assert result.data is None
    assert result.error == "Repository contents lookup failed: GitHub unavailable"



def test_tool_dispatcher_search_code():
    executor = Mock()
    executor.search_code.return_value = {
        "total_count": 1,
        "incomplete_results": False,
        "items": [
            {
                "name": "config.py",
                "path": "app/config.py",
                "repository": {
                    "full_name": "microsoft/vscode",
                },
            }
        ],
    }

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "search_code",
        {
            "query": "password",
            "page": 1,
            "per_page": 10,
        },
    )

    assert result.tool_name == "search_code"
    assert result.success is True
    assert result.data["total_count"] == 1
    assert result.data["items"][0]["name"] == "config.py"
    assert result.error is None

    executor.search_code.assert_called_once_with(
        query="password",
        page=1,
        per_page=10,
    )



def test_tool_dispatcher_search_code_returns_error_result_on_failure():
    executor = Mock()
    executor.search_code.side_effect = ToolExecutionError(
        "Code search failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "search_code",
        {
            "query": "password",
            "page": 1,
            "per_page": 10,
        },
    )

    assert result.tool_name == "search_code"
    assert result.success is False
    assert result.data is None
    assert result.error == "Code search failed: GitHub unavailable"



def test_validate_get_file_arguments_accepts_valid_arguments():
    validate_get_file_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
            "path": "src/main.py",
        }
    )


def test_validate_get_file_arguments_rejects_empty_owner():
    with pytest.raises(
        ValueError,
        match="Repository owner cannot be empty",
    ):
        validate_get_file_arguments(
            {
                "owner": "",
                "repo": "vscode",
                "path": "src/main.py",
            }
        )


def test_validate_get_file_arguments_rejects_empty_repo():
    with pytest.raises(
        ValueError,
        match="Repository name cannot be empty",
    ):
        validate_get_file_arguments(
            {
                "owner": "microsoft",
                "repo": "",
                "path": "src/main.py",
            }
        )


def test_validate_get_file_arguments_rejects_empty_path():
    with pytest.raises(
        ValueError,
        match="File path cannot be empty",
    ):
        validate_get_file_arguments(
            {
                "owner": "microsoft",
                "repo": "vscode",
                "path": "",
            }
        )



def test_tool_dispatcher_get_file():
    executor = Mock()
    executor.get_file.return_value = {
        "name": "main.py",
        "path": "src/main.py",
        "type": "file",
        "content": "print('hello')",
    }

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_file",
        {
            "owner": "microsoft",
            "repo": "vscode",
            "path": "src/main.py",
        },
    )

    assert result.tool_name == "get_file"
    assert result.success is True
    assert result.data["name"] == "main.py"
    assert result.data["path"] == "src/main.py"
    assert result.error is None

    executor.get_file.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
        path="src/main.py",
    )



def test_tool_dispatcher_get_file_returns_error_result_on_failure():
    executor = Mock()
    executor.get_file.side_effect = ToolExecutionError(
        "File lookup failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_file",
        {
            "owner": "microsoft",
            "repo": "vscode",
            "path": "src/main.py",
        },
    )

    assert result.tool_name == "get_file"
    assert result.success is False
    assert result.data is None
    assert result.error == "File lookup failed: GitHub unavailable"



def test_validate_get_commits_arguments_accepts_valid_arguments():
    validate_get_commits_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
        }
    )


def test_validate_get_commits_arguments_rejects_empty_owner():
    with pytest.raises(
        ValueError,
        match="Repository owner cannot be empty",
    ):
        validate_get_commits_arguments(
            {
                "owner": "",
                "repo": "vscode",
            }
        )


def test_validate_get_commits_arguments_rejects_empty_repo():
    with pytest.raises(
        ValueError,
        match="Repository name cannot be empty",
    ):
        validate_get_commits_arguments(
            {
                "owner": "microsoft",
                "repo": "",
            }
        )



def test_tool_dispatcher_get_commits():
    executor = Mock()
    executor.get_commits.return_value = [
        {
            "sha": "abc123",
            "commit": {
                "message": "Initial commit",
            },
        }
    ]

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_commits",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_commits"
    assert result.success is True
    assert result.data[0]["sha"] == "abc123"
    assert result.data[0]["commit"]["message"] == "Initial commit"
    assert result.error is None

    executor.get_commits.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
    )



def test_tool_dispatcher_get_commits_returns_error_result_on_failure():
    executor = Mock()
    executor.get_commits.side_effect = ToolExecutionError(
        "Commit lookup failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_commits",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_commits"
    assert result.success is False
    assert result.data is None
    assert result.error == "Commit lookup failed: GitHub unavailable"



def test_validate_get_branches_arguments_accepts_valid_arguments():
    validate_get_branches_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
        }
    )


def test_validate_get_branches_arguments_rejects_empty_owner():
    with pytest.raises(
        ValueError,
        match="Repository owner cannot be empty",
    ):
        validate_get_branches_arguments(
            {
                "owner": "",
                "repo": "vscode",
            }
        )


def test_validate_get_branches_arguments_rejects_empty_repo():
    with pytest.raises(
        ValueError,
        match="Repository name cannot be empty",
    ):
        validate_get_branches_arguments(
            {
                "owner": "microsoft",
                "repo": "",
            }
        )


def test_tool_dispatcher_get_branches():
    executor = Mock()
    executor.get_branches.return_value = [
        {
            "name": "main",
            "protected": False,
        },
        {
            "name": "develop",
            "protected": True,
        },
    ]

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_branches",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_branches"
    assert result.success is True
    assert result.data[0]["name"] == "main"
    assert result.data[1]["name"] == "develop"
    assert result.error is None

    executor.get_branches.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
    )


def test_tool_dispatcher_get_branches_returns_error_result_on_failure():
    executor = Mock()
    executor.get_branches.side_effect = ToolExecutionError(
        "Branch lookup failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_branches",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_branches"
    assert result.success is False
    assert result.data is None
    assert result.error == "Branch lookup failed: GitHub unavailable"



def test_validate_get_pull_requests_arguments_accepts_valid_arguments():
    validate_get_pull_requests_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
        }
    )


def test_validate_get_pull_requests_arguments_rejects_empty_owner():
    with pytest.raises(
        ValueError,
        match="Repository owner cannot be empty",
    ):
        validate_get_pull_requests_arguments(
            {
                "owner": "",
                "repo": "vscode",
            }
        )


def test_validate_get_pull_requests_arguments_rejects_empty_repo():
    with pytest.raises(
        ValueError,
        match="Repository name cannot be empty",
    ):
        validate_get_pull_requests_arguments(
            {
                "owner": "microsoft",
                "repo": "",
            }
        )


def test_tool_dispatcher_get_pull_requests():
    executor = Mock()
    executor.get_pull_requests.return_value = [
        {
            "number": 123,
            "title": "Improve documentation",
            "state": "open",
        },
        {
            "number": 124,
            "title": "Fix configuration",
            "state": "closed",
        },
    ]

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_pull_requests",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_pull_requests"
    assert result.success is True
    assert result.data[0]["number"] == 123
    assert result.data[0]["title"] == "Improve documentation"
    assert result.data[1]["state"] == "closed"
    assert result.error is None

    executor.get_pull_requests.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
    )



def test_tool_dispatcher_get_pull_requests_returns_error_result_on_failure():
    executor = Mock()
    executor.get_pull_requests.side_effect = ToolExecutionError(
        "Pull request lookup failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_pull_requests",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_pull_requests"
    assert result.success is False
    assert result.data is None
    assert result.error == "Pull request lookup failed: GitHub unavailable"



def test_validate_get_contributors_arguments_accepts_valid_arguments():
    validate_get_contributors_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
        }
    )


def test_validate_get_contributors_arguments_rejects_empty_owner():
    with pytest.raises(
        ValueError,
        match="Repository owner cannot be empty",
    ):
        validate_get_contributors_arguments(
            {
                "owner": "",
                "repo": "vscode",
            }
        )


def test_validate_get_contributors_arguments_rejects_empty_repo():
    with pytest.raises(
        ValueError,
        match="Repository name cannot be empty",
    ):
        validate_get_contributors_arguments(
            {
                "owner": "microsoft",
                "repo": "",
            }
        )



def test_tool_dispatcher_get_contributors():
    executor = Mock()
    executor.get_contributors.return_value = [
        {
            "login": "developer-one",
            "contributions": 42,
        },
        {
            "login": "developer-two",
            "contributions": 18,
        },
    ]

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_contributors",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_contributors"
    assert result.success is True
    assert result.data[0]["login"] == "developer-one"
    assert result.data[0]["contributions"] == 42
    assert result.data[1]["login"] == "developer-two"
    assert result.error is None

    executor.get_contributors.assert_called_once_with(
        owner="microsoft",
        repo="vscode",
    )



def test_tool_dispatcher_get_contributors_returns_error_result_on_failure():
    executor = Mock()
    executor.get_contributors.side_effect = ToolExecutionError(
        "Contributor lookup failed: GitHub unavailable"
    )

    dispatcher = ToolDispatcher(
        executor,
        ToolRegistry(),
    )

    result = dispatcher.dispatch(
        "get_contributors",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.tool_name == "get_contributors"
    assert result.success is False
    assert result.data is None
    assert result.error == "Contributor lookup failed: GitHub unavailable"



def test_validate_get_releases_arguments_accepts_valid_arguments():
    validate_get_releases_arguments(
        {
            "owner": "microsoft",
            "repo": "vscode",
        }
    )


def test_validate_get_releases_arguments_rejects_empty_owner():
    with pytest.raises(
        ValueError,
        match="Repository owner cannot be empty",
    ):
        validate_get_releases_arguments(
            {
                "owner": "",
                "repo": "vscode",
            }
        )


def test_validate_get_releases_arguments_rejects_empty_repo():
    with pytest.raises(
        ValueError,
        match="Repository name cannot be empty",
    ):
        validate_get_releases_arguments(
            {
                "owner": "microsoft",
                "repo": "",
            }
        )



def test_dispatch_get_releases_success(monkeypatch):
    class FakeExecutor:
        def get_releases(self, owner, repo):
            return [
                {
                    "tag_name": "v1.0.0",
                    "name": "Initial Release",
                }
            ]

    fake_executor = FakeExecutor()
    registry = ToolRegistry()
    dispatcher = ToolDispatcher(fake_executor, registry)

    result = dispatcher.dispatch(
        "get_releases",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.success is True
    assert result.data == [
        {
            "tag_name": "v1.0.0",
            "name": "Initial Release",
        }
    ]



def test_dispatch_get_releases_error():
    class FakeExecutor:
        def get_releases(self, owner, repo):
            raise ToolExecutionError("Release lookup failed")

    fake_executor = FakeExecutor()
    registry = ToolRegistry()
    dispatcher = ToolDispatcher(fake_executor, registry)

    result = dispatcher.dispatch(
        "get_releases",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.success is False
    assert result.tool_name == "get_releases"
    assert result.error == "Release lookup failed"