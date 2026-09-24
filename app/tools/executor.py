from app.github.client import GitHubClient
from app.tools.errors import ToolExecutionError


class ToolExecutor:
    def __init__(self, client: GitHubClient):
        self.client = client

    def search_repositories(
        self,
        query: str,
        page: int = 1,
        per_page: int = 30,
    ) -> dict:
        try:
            return self.client.search_repositories(
                query=query,
                page=page,
                per_page=per_page,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Repository search failed: {exc}"
            ) from exc



    def search_code(
        self,
        query: str,
        page: int = 1,
        per_page: int = 30,
    ) -> dict:
        try:
            return self.client.search_code(
                query=query,
                page=page,
                per_page=per_page,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Code search failed: {exc}"
            ) from exc

        

    def get_repository(
        self,
        owner: str,
        repo: str,
    ) -> dict:
        try:
            return self.client.get_repository(
                owner=owner,
                repo=repo,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Repository lookup failed: {exc}"
            ) from exc


    def get_repository_contents(
        self,
        owner: str,
        repo: str,
        path: str = "",
    ) -> dict | list:
        try:
            return self.client.get_repository_contents(
                owner=owner,
                repo=repo,
                path=path,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Repository contents lookup failed: {exc}"
            ) from exc



    def get_file(
        self,
        owner: str,
        repo: str,
        path: str,
    ) -> dict | list:
        try:
            return self.client.get_file(
                owner=owner,
                repo=repo,
                path=path,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"File lookup failed: {exc}"
            ) from exc


    def get_commits(
        self,
        owner: str,
        repo: str,
    ) -> list:
        try:
            return self.client.get_commits(
                owner=owner,
                repo=repo,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Commit lookup failed: {exc}"
            ) from exc


    def get_branches(
        self,
        owner: str,
        repo: str,
    ) -> list:
        try:
            return self.client.get_branches(
                owner=owner,
                repo=repo,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Branch lookup failed: {exc}"
            ) from exc



    def get_pull_requests(
        self,
        owner: str,
        repo: str,
    ) -> list:
        try:
            return self.client.get_pull_requests(
                owner=owner,
                repo=repo,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Pull request lookup failed: {exc}"
            ) from exc


    def get_contributors(
        self,
        owner: str,
        repo: str,
    ) -> list:
        try:
            return self.client.get_contributors(
                owner=owner,
                repo=repo,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Contributor lookup failed: {exc}"
            ) from exc


    def get_releases(
        self,
        owner: str,
        repo: str,
    ) -> list:
        try:
            return self.client.get_releases(
                owner=owner,
                repo=repo,
            )
        except Exception as exc:
            raise ToolExecutionError(
                f"Release lookup failed: {exc}"
            ) from exc