from app.models.repository import RepositoryCandidate


def test_repository_candidate():
    repository = RepositoryCandidate(
        full_name="microsoft/vscode",
        owner_login="microsoft",
        html_url="https://github.com/microsoft/vscode",
        description="Visual Studio Code",
        fork=False,
        default_branch="main",
    )

    assert repository.full_name == "microsoft/vscode"
    assert repository.owner_login == "microsoft"
    assert repository.html_url == "https://github.com/microsoft/vscode"
    assert repository.description == "Visual Studio Code"
    assert repository.fork is False
    assert repository.default_branch == "main"


def test_repository_candidate_from_github_data():
    data = {
        "full_name": "microsoft/vscode",
        "owner": {
            "login": "microsoft",
        },
        "html_url": "https://github.com/microsoft/vscode",
        "description": "Visual Studio Code",
        "fork": False,
        "default_branch": "main",
    }

    repository = RepositoryCandidate.from_github_data(data)

    assert repository == RepositoryCandidate(
        full_name="microsoft/vscode",
        owner_login="microsoft",
        html_url="https://github.com/microsoft/vscode",
        description="Visual Studio Code",
        fork=False,
        default_branch="main",
    )


def test_repository_candidates_from_github_data():
    data = [
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
    ]

    repositories = RepositoryCandidate.from_github_data_list(data)

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