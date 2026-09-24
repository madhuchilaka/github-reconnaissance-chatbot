from app.github.client import GitHubClient
from app.models.repository import RepositoryCandidate
from app.models.repository_metadata import RepositoryMetadata


class RepositoryService:
    @staticmethod
    def to_candidates(search_result: dict) -> list[RepositoryCandidate]:
        items = search_result.get("items", [])
        return RepositoryCandidate.from_github_data_list(items)

    @staticmethod
    def search_repositories(
        client: GitHubClient,
        query: str,
    ) -> list[RepositoryCandidate]:
        search_result = client.search_repositories(query)
        return RepositoryService.to_candidates(search_result)

    @staticmethod
    def get_repository_metadata(
        client: GitHubClient,
        owner: str,
        repo: str,
    ) -> RepositoryMetadata:
        repository_data = client.get_repository(owner, repo)
        return RepositoryMetadata.from_github_data(repository_data)