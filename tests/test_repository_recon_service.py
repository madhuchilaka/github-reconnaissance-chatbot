from unittest.mock import Mock

from app.models.repository_metadata import RepositoryMetadata
from app.services.repository_recon_service import RepositoryReconService


def test_collect_metadata():
    client = Mock()

    client.get_repository.return_value = {
        "id": 1,
        "full_name": "example/project",
        "owner": {"login": "example"},
        "html_url": "https://github.com/example/project",
        "description": "Example project",
        "default_branch": "main",
        "visibility": "public",
        "language": "Python",
        "topics": [],
        "fork": False,
        "archived": False,
        "stargazers_count": 10,
        "forks_count": 2,
        "open_issues_count": 1,
        "created_at": None,
        "updated_at": None,
        "pushed_at": None,
    }

    service = RepositoryReconService(client)

    result = service.collect_metadata("example", "project")

    assert result == RepositoryMetadata(
        id=1,
        full_name="example/project",
        owner_login="example",
        html_url="https://github.com/example/project",
        description="Example project",
        default_branch="main",
        visibility="public",
        language="Python",
        topics=[],
        fork=False,
        archived=False,
        stargazers_count=10,
        forks_count=2,
        open_issues_count=1,
        created_at=None,
        updated_at=None,
        pushed_at=None,
    )

    client.get_repository.assert_called_once_with(
        "example",
        "project",
    )
from unittest.mock import Mock

from app.services.repository_recon_service import RepositoryReconService


def test_collect_contents_returns_directory_contents():
    client = Mock()

    client.get_repository_contents.return_value = [
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
        },
        {
            "name": "app",
            "path": "app",
            "type": "dir",
        },
    ]

    service = RepositoryReconService(client)

    result = service.collect_contents(
        "example",
        "project",
    )

    assert result == [
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
        },
        {
            "name": "app",
            "path": "app",
            "type": "dir",
        },
    ]

    client.get_repository_contents.assert_called_once_with(
        "example",
        "project",
        "",
    )
from unittest.mock import Mock

from app.services.repository_recon_service import RepositoryReconService


def test_collect_branches():
    client = Mock()

    client.get_branches.return_value = [
        {
            "name": "main",
            "protected": False,
        },
        {
            "name": "develop",
            "protected": True,
        },
    ]

    service = RepositoryReconService(client)

    result = service.collect_branches(
        "example",
        "project",
    )

    assert result == [
        {
            "name": "main",
            "protected": False,
        },
        {
            "name": "develop",
            "protected": True,
        },
    ]

    client.get_branches.assert_called_once_with(
        "example",
        "project",
    )
from unittest.mock import Mock

from app.services.repository_recon_service import RepositoryReconService


def test_collect_commits():
    client = Mock()

    client.get_commits.return_value = [
        {
            "sha": "abc123",
            "commit": {
                "message": "Initial commit",
            },
        }
    ]

    service = RepositoryReconService(client)

    result = service.collect_commits(
        "example",
        "project",
    )

    assert result == [
        {
            "sha": "abc123",
            "commit": {
                "message": "Initial commit",
            },
        }
    ]

    client.get_commits.assert_called_once_with(
        "example",
        "project",
    )

def test_collect_pull_requests():
    client = Mock()

    client.get_pull_requests.return_value = [
        {
            "number": 1,
            "title": "Add feature",
            "state": "open",
        }
    ]

    service = RepositoryReconService(client)

    result = service.collect_pull_requests(
        "example",
        "project",
    )

    assert result == [
        {
            "number": 1,
            "title": "Add feature",
            "state": "open",
        }
    ]

    client.get_pull_requests.assert_called_once_with(
        "example",
        "project",
    )

def test_collect_contributors():
    client = Mock()

    client.get_contributors.return_value = [
        {
            "login": "developer1",
            "contributions": 25,
        }
    ]

    service = RepositoryReconService(client)

    result = service.collect_contributors(
        "example",
        "project",
    )

    assert result == [
        {
            "login": "developer1",
            "contributions": 25,
        }
    ]

    client.get_contributors.assert_called_once_with(
        "example",
        "project",
    )

def test_collect_releases():
    client = Mock()

    client.get_releases.return_value = [
        {
            "tag_name": "v1.0.0",
            "name": "Initial Release",
        }
    ]

    service = RepositoryReconService(client)

    result = service.collect_releases(
        "example",
        "project",
    )

    assert result == [
        {
            "tag_name": "v1.0.0",
            "name": "Initial Release",
        }
    ]

    client.get_releases.assert_called_once_with(
        "example",
        "project",
    )

def test_collect_repository():
    client = Mock()

    metadata = Mock()

    client.get_repository_contents.return_value = [
        {"name": "README.md"}
    ]
    client.get_branches.return_value = [
        {"name": "main"}
    ]
    client.get_commits.return_value = [
        {"sha": "abc123"}
    ]
    client.get_pull_requests.return_value = [
        {"number": 1}
    ]
    client.get_contributors.return_value = [
        {"login": "developer1"}
    ]
    client.get_releases.return_value = [
        {"tag_name": "v1.0.0"}
    ]

    service = RepositoryReconService(client)

    service.collect_metadata = Mock(return_value=metadata)

    result = service.collect_repository(
        "example",
        "project",
    )

    assert result.metadata is metadata
    assert result.contents == [{"name": "README.md"}]
    assert result.branches == [{"name": "main"}]
    assert result.commits == [{"sha": "abc123"}]
    assert result.pull_requests == [{"number": 1}]
    assert result.contributors == [{"login": "developer1"}]
    assert result.releases == [{"tag_name": "v1.0.0"}]

    service.collect_metadata.assert_called_once_with(
        "example",
        "project",
    )
    client.get_repository_contents.assert_called_once_with(
        "example",
        "project",
        "",
    )
    client.get_branches.assert_called_once_with(
        "example",
        "project",
    )
    client.get_commits.assert_called_once_with(
        "example",
        "project",
    )
    client.get_pull_requests.assert_called_once_with(
        "example",
        "project",
    )
    client.get_contributors.assert_called_once_with(
        "example",
        "project",
    )
    client.get_releases.assert_called_once_with(
        "example",
        "project",
    )

def test_collect_contents_recursively():
    client = Mock()

    client.get_repository_contents.side_effect = [
        [
            {
                "name": "README.md",
                "path": "README.md",
                "type": "file",
            },
            {
                "name": "app",
                "path": "app",
                "type": "dir",
            },
        ],
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            },
            {
                "name": "utils.py",
                "path": "app/utils.py",
                "type": "file",
            },
        ],
    ]

    service = RepositoryReconService(client)

    result = service.collect_contents_recursively(
        "example",
        "project",
    )

    assert result == [
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
        },
        {
            "name": "main.py",
            "path": "app/main.py",
            "type": "file",
        },
        {
            "name": "utils.py",
            "path": "app/utils.py",
            "type": "file",
        },
    ]

    assert client.get_repository_contents.call_count == 2
    client.get_repository_contents.assert_any_call(
        "example",
        "project",
        "",
    )
    client.get_repository_contents.assert_any_call(
        "example",
        "project",
        "app",
    )



def test_load_file():
    client = Mock()

    client.get_file.return_value = {
        "name": "package.json",
        "path": "package.json",
        "type": "file",
        "content": "eyJkZXBlbmRlbmNpZXMiOiB7fX0=",
        "encoding": "base64",
    }

    service = RepositoryReconService(client)

    result = service.load_file(
        "example",
        "project",
        "package.json",
    )

    assert result == {
        "name": "package.json",
        "path": "package.json",
        "type": "file",
        "content": "eyJkZXBlbmRlbmNpZXMiOiB7fX0=",
        "encoding": "base64",
    }

    client.get_file.assert_called_once_with(
        "example",
        "project",
        "package.json",
    )





def test_collect_repository_for_analysis():
    client = Mock()

    metadata = Mock(default_branch="main")

    service = RepositoryReconService(client)
    service.collect_metadata = Mock(return_value=metadata)
    service.collect_contents_from_tree = Mock(
        return_value=[
            {
                "name": "README.md",
                "path": "README.md",
                "type": "file",
                "sha": "blob123",
                "size": 100,
            },
        ]
    )

    result = service.collect_repository_for_analysis(
        "example",
        "project",
    )

    assert result.metadata is metadata
    assert result.contents == [
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
            "sha": "blob123",
            "size": 100,
        },
    ]

    assert result.branches == []
    assert result.commits == []
    assert result.pull_requests == []
    assert result.contributors == []
    assert result.releases == []

    service.collect_metadata.assert_called_once_with(
        "example",
        "project",
    )

    service.collect_contents_from_tree.assert_called_once_with(
        "example",
        "project",
        "main",
    )

    client.get_repository_contents.assert_not_called()
    client.get_branches.assert_not_called()
    client.get_commits.assert_not_called()
    client.get_pull_requests.assert_not_called()
    client.get_contributors.assert_not_called()
    client.get_releases.assert_not_called()



def test_collect_repository_for_analysis_propagates_github_api_error():
    from app.github.exceptions import GitHubAPIError

    client = Mock()

    expected_error = GitHubAPIError(
        status_code=500,
        message="GitHub API request failed with status 500",
    )

    service = RepositoryReconService(client)

    service.collect_metadata = Mock(side_effect=expected_error)

    try:
        service.collect_repository_for_analysis(
            "example",
            "project",
        )
    except GitHubAPIError as error:
        assert error is expected_error
        assert error.status_code == 500
        assert error.is_retryable is True
    else:
        raise AssertionError(
            "Expected GitHubAPIError to be propagated"
        )




def test_collect_contents_from_tree():
    client = Mock()

    service = RepositoryReconService(client)

    service.collect_metadata = Mock(
        return_value=Mock(default_branch="main")
    )

    client.get_tree.return_value = {
        "sha": "tree123",
        "tree": [
            {
                "path": "README.md",
                "mode": "100644",
                "type": "blob",
                "sha": "blob123",
                "size": 100,
            },
            {
                "path": "app",
                "mode": "040000",
                "type": "tree",
                "sha": "dir123",
            },
            {
                "path": "app/main.py",
                "mode": "100644",
                "type": "blob",
                "sha": "blob456",
                "size": 200,
            },
        ],
        "truncated": False,
    }

    result = service.collect_contents_from_tree(
        "example",
        "project",
        "main",
    )

    assert result == [
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
            "sha": "blob123",
            "size": 100,
        },
        {
            "name": "main.py",
            "path": "app/main.py",
            "type": "file",
            "sha": "blob456",
            "size": 200,
        },
    ]

    client.get_tree.assert_called_once_with(
        "example",
        "project",
        "main",
    )

def test_load_blob():
    client = Mock()

    client.get_blob.return_value = {
        "sha": "blob123",
        "size": 12,
        "content": "SGVsbG8gV29ybGQ=",
        "encoding": "base64",
    }

    service = RepositoryReconService(client)

    result = service.load_blob(
        "example",
        "project",
        "blob123",
    )

    assert result == {
        "sha": "blob123",
        "size": 12,
        "content": "SGVsbG8gV29ybGQ=",
        "encoding": "base64",
    }

    client.get_blob.assert_called_once_with(
        "example",
        "project",
        "blob123",
    )

def test_collect_repository_for_analysis_uses_tree():
    client = Mock()

    metadata = Mock(default_branch="main")

    service = RepositoryReconService(client)
    service.collect_metadata = Mock(return_value=metadata)
    service.collect_contents_from_tree = Mock(
        return_value=[
            {
                "name": "README.md",
                "path": "README.md",
                "type": "file",
                "sha": "blob123",
                "size": 100,
            },
        ]
    )

    result = service.collect_repository_for_analysis(
        "example",
        "project",
    )

    assert result.metadata is metadata
    assert result.contents == [
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
            "sha": "blob123",
            "size": 100,
        },
    ]

    service.collect_metadata.assert_called_once_with(
        "example",
        "project",
    )

    service.collect_contents_from_tree.assert_called_once_with(
        "example",
        "project",
        "main",
    )

    client.get_repository_contents.assert_not_called()
    client.get_branches.assert_not_called()
    client.get_commits.assert_not_called()
    client.get_pull_requests.assert_not_called()
    client.get_contributors.assert_not_called()
    client.get_releases.assert_not_called()