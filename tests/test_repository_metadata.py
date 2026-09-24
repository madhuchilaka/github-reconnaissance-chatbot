from app.models.repository_metadata import RepositoryMetadata


def test_repository_metadata_from_github_data():
    data = {
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

    repository = RepositoryMetadata.from_github_data(data)

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



def test_repository_metadata_from_github_data_handles_optional_fields():
    data = {
        "id": 123,
        "full_name": "example/repository",
        "owner": {
            "login": "example",
        },
        "html_url": "https://github.com/example/repository",
        "description": None,
        "default_branch": "main",
        "fork": False,
        "archived": False,
        "stargazers_count": 0,
        "forks_count": 0,
        "open_issues_count": 0,
    }

    repository = RepositoryMetadata.from_github_data(data)

    assert repository.description is None
    assert repository.visibility is None
    assert repository.language is None
    assert repository.topics == []
    assert repository.created_at is None
    assert repository.updated_at is None
    assert repository.pushed_at is None