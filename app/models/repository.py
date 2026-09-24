from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryCandidate:
    full_name: str
    owner_login: str
    html_url: str
    description: str | None
    fork: bool
    default_branch: str

    @classmethod
    def from_github_data(cls, data: dict) -> "RepositoryCandidate":
        return cls(
            full_name=data["full_name"],
            owner_login=data["owner"]["login"],
            html_url=data["html_url"],
            description=data.get("description"),
            fork=data["fork"],
            default_branch=data["default_branch"],
        )

    @classmethod
    def from_github_data_list(
        cls,
        data: list[dict],
    ) -> list["RepositoryCandidate"]:
        return [cls.from_github_data(item) for item in data]