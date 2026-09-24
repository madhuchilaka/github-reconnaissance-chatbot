from app.github.client import GitHubClient
from app.models.repository_recon import RepositoryReconData
from app.services.repository_service import RepositoryService


class RepositoryReconService:
    def __init__(self, client: GitHubClient) -> None:
        self.client = client

    def collect_metadata(
        self,
        owner: str,
        repo: str,
    ):
        return RepositoryService.get_repository_metadata(
            self.client,
            owner,
            repo,
        )

    def collect_contents(
        self,
        owner: str,
        repo: str,
        path: str = "",
    ) -> list[dict]:
        result = self.client.get_repository_contents(
            owner,
            repo,
            path,
        )

        if isinstance(result, list):
            return result

        return [result]

    def collect_branches(
        self,
        owner: str,
        repo: str,
    ) -> list[dict]:
        return self.client.get_branches(
            owner,
            repo,
        )

    def collect_commits(
        self,
        owner: str,
        repo: str,
    ) -> list[dict]:
        return self.client.get_commits(
            owner,
            repo,
        )

    def collect_pull_requests(
        self,
        owner: str,
        repo: str,
    ) -> list[dict]:
        return self.client.get_pull_requests(
            owner,
            repo,
        )

    def collect_contributors(
        self,
        owner: str,
        repo: str,
    ) -> list[dict]:
        return self.client.get_contributors(
            owner,
            repo,
        )

    def collect_releases(
        self,
        owner: str,
        repo: str,
    ) -> list[dict]:
        return self.client.get_releases(
            owner,
            repo,
        )

    def collect_repository(
        self,
        owner: str,
        repo: str,
    ) -> RepositoryReconData:
        return RepositoryReconData(
            metadata=self.collect_metadata(owner, repo),
            contents=self.collect_contents_recursively(owner, repo),
            branches=self.collect_branches(owner, repo),
            commits=self.collect_commits(owner, repo),
            pull_requests=self.collect_pull_requests(owner, repo),
            contributors=self.collect_contributors(owner, repo),
            releases=self.collect_releases(owner, repo),
        )

    def collect_contents_recursively(
        self,
        owner: str,
        repo: str,
        path: str = "",
    ) -> list[dict]:
        items = self.collect_contents(
            owner,
            repo,
            path,
        )

        files = []
        directories = []

        for item in items:
            if item.get("type") == "dir":
                directories.append(item)
            else:
                files.append(item)

        for directory in directories:
            files.extend(
                self.collect_contents_recursively(
                    owner,
                    repo,
                    directory["path"],
                )
            )

        return files

    def load_file(
        self,
        owner: str,
        repo: str,
        path: str,
    ) -> dict | list:
        return self.client.get_file(
            owner,
            repo,
            path,
        )