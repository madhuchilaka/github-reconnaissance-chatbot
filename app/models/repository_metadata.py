from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryMetadata:
    id: int
    full_name: str
    owner_login: str
    html_url: str
    description: str | None
    default_branch: str
    visibility: str | None
    language: str | None
    topics: list[str]
    fork: bool
    archived: bool
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    created_at: str | None
    updated_at: str | None
    pushed_at: str | None

    @classmethod
    def from_github_data(cls, data: dict) -> "RepositoryMetadata":
        return cls(
            id=data["id"],
            full_name=data["full_name"],
            owner_login=data["owner"]["login"],
            html_url=data["html_url"],
            description=data.get("description"),
            default_branch=data["default_branch"],
            visibility=data.get("visibility"),
            language=data.get("language"),
            topics=data.get("topics", []),
            fork=data["fork"],
            archived=data["archived"],
            stargazers_count=data["stargazers_count"],
            forks_count=data["forks_count"],
            open_issues_count=data["open_issues_count"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            pushed_at=data.get("pushed_at"),
        )
