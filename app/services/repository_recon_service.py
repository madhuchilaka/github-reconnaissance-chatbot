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

    def collect_repository_for_analysis(
        self,
        owner: str,
        repo: str,
    ) -> RepositoryReconData:
        metadata = self.collect_metadata(
            owner,
            repo,
        )

        return RepositoryReconData(
            metadata=metadata,
            contents=self.collect_contents_from_tree(
                owner,
                repo,
                metadata.default_branch,
            ),
            branches=[],
            commits=[],
            pull_requests=[],
            contributors=[],
            releases=[],
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

    def collect_contents_from_tree(
        self,
        owner: str,
        repo: str,
        tree_sha: str,
    ) -> list[dict]:
        tree_data = self.client.get_tree(
            owner,
            repo,
            tree_sha,
        )

        files = []

        for item in tree_data.get("tree", []):
            if item.get("type") != "blob":
                continue

            path = item["path"]

            files.append(
                {
                    "name": path.rsplit("/", 1)[-1],
                    "path": path,
                    "type": "file",
                    "sha": item["sha"],
                    "size": item.get("size"),
                }
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

    def load_blob(
        self,
        owner: str,
        repo: str,
        blob_sha: str,
    ):
        return self.client.get_blob(
            owner,
            repo,
            blob_sha,
        )
