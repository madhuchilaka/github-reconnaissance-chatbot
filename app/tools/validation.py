def validate_search_repositories_arguments(arguments: dict) -> None:
    query = arguments.get("query")

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Repository search query cannot be empty")

    page = arguments.get("page", 1)

    if not isinstance(page, int) or isinstance(page, bool) or page < 1:
        raise ValueError("Page must be a positive integer")

    per_page = arguments.get("per_page", 30)

    if (
        not isinstance(per_page, int)
        or isinstance(per_page, bool)
        or per_page < 1
        or per_page > 100
    ):
        raise ValueError("per_page must be an integer between 1 and 100")



def validate_search_code_arguments(arguments: dict) -> None:
    query = arguments.get("query")

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Code search query cannot be empty")

    page = arguments.get("page", 1)

    if not isinstance(page, int) or isinstance(page, bool) or page < 1:
        raise ValueError("Page must be a positive integer")

    per_page = arguments.get("per_page", 30)

    if (
        not isinstance(per_page, int)
        or isinstance(per_page, bool)
        or per_page < 1
        or per_page > 100
    ):
        raise ValueError("per_page must be an integer between 1 and 100")



def validate_get_repository_arguments(arguments: dict) -> None:
    owner = arguments.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        raise ValueError("Repository owner cannot be empty")

    repo = arguments.get("repo")

    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("Repository name cannot be empty")



def validate_get_repository_contents_arguments(arguments: dict) -> None:
    owner = arguments.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        raise ValueError("Repository owner cannot be empty")

    repo = arguments.get("repo")

    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("Repository name cannot be empty")

    path = arguments.get("path", "")

    if not isinstance(path, str):
        raise ValueError("Repository path must be a string")


def validate_get_file_arguments(arguments: dict) -> None:
    owner = arguments.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        raise ValueError("Repository owner cannot be empty")

    repo = arguments.get("repo")

    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("Repository name cannot be empty")

    path = arguments.get("path")

    if not isinstance(path, str) or not path.strip():
        raise ValueError("File path cannot be empty")



def validate_get_commits_arguments(arguments: dict) -> None:
    owner = arguments.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        raise ValueError("Repository owner cannot be empty")

    repo = arguments.get("repo")

    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("Repository name cannot be empty")



def validate_get_branches_arguments(arguments: dict) -> None:
    owner = arguments.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        raise ValueError("Repository owner cannot be empty")

    repo = arguments.get("repo")

    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("Repository name cannot be empty")


def validate_get_pull_requests_arguments(arguments: dict) -> None:
    owner = arguments.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        raise ValueError("Repository owner cannot be empty")

    repo = arguments.get("repo")

    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("Repository name cannot be empty")


def validate_get_contributors_arguments(arguments: dict) -> None:
    owner = arguments.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        raise ValueError("Repository owner cannot be empty")

    repo = arguments.get("repo")

    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("Repository name cannot be empty")



def validate_get_releases_arguments(arguments: dict) -> None:
    owner = arguments.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        raise ValueError("Repository owner cannot be empty")

    repo = arguments.get("repo")

    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("Repository name cannot be empty")