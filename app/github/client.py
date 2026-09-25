
import time
import httpx

from app.config.settings import (
    GITHUB_API_BASE_URL,
    GITHUB_API_TIMEOUT,
    GITHUB_MAX_RETRIES,
    GITHUB_RETRY_BACKOFF,
    GITHUB_TOKEN,
)

from app.github.exceptions import GitHubAPIError

class GitHubClient:
    def __init__(self, client: httpx.Client | None = None):
        headers = {
            "Accept": "application/vnd.github+json",
        }
        
        self.max_retries = GITHUB_MAX_RETRIES
        self.retry_backoff = GITHUB_RETRY_BACKOFF

        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

        self.client = client or httpx.Client(
            base_url=GITHUB_API_BASE_URL,
            timeout=GITHUB_API_TIMEOUT,
            headers=headers,
        )

    def close(self) -> None:
        self.client.close()


    def _get_retry_delay(self, attempt: int) -> float:
        return self.retry_backoff * (2 ** attempt)


    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
    ) -> httpx.Response:
        for attempt in range(self.max_retries + 1):
            response = self.client.request(
                method,
                endpoint,
                params=params,
            )

            if response.status_code < 400:
                return response

            retry_after = response.headers.get("Retry-After")

            if retry_after is not None:
                retry_after = float(retry_after)

            error = GitHubAPIError(
                response.status_code,
                f"GitHub API request failed with status {response.status_code}",
                retry_after,
            )

            if not error.is_retryable or attempt == self.max_retries:
                raise error

            delay = (
                error.retry_after
                if error.retry_after is not None
                else self._get_retry_delay(attempt)
            )

            time.sleep(delay)

        raise RuntimeError("GitHub API request failed unexpectedly")


    def _request_json(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
    ) -> dict | list:
        response = self._request(
            method,
            endpoint,
            params=params,
        )

        return response.json()

    

    def get_repository(self, owner: str, repo: str) -> dict:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        return self._request_json(
            "GET",
            f"/repos/{owner}/{repo}",
        )


    def get_repository_contents(
        self,
        owner: str,
        repo: str,
        path: str = "",
    ) -> dict | list:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        endpoint = f"/repos/{owner}/{repo}/contents/{path}"

        return self._request_json(
            "GET",
            endpoint,
        )


    def get_file(
        self,
        owner: str,
        repo: str,
        path: str,
    ) -> dict | list:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        if not path:
            raise ValueError("File path cannot be empty")

        endpoint = f"/repos/{owner}/{repo}/contents/{path}"

        return self._request_json(
            "GET",
            endpoint,
        )


    def get_tree(
        self,
        owner: str,
        repo: str,
        tree_sha: str,
    ) -> dict:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        if not tree_sha:
            raise ValueError("Tree SHA cannot be empty")

        return self._request_json(
            "GET",
            f"/repos/{owner}/{repo}/git/trees/{tree_sha}",
            params={"recursive": "1"},
        )

    def get_blob(
        self,
        owner: str,
        repo: str,
        blob_sha: str,
    ) -> dict:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        if not blob_sha:
            raise ValueError("Blob SHA cannot be empty")

        return self._request_json(
            "GET",
            f"/repos/{owner}/{repo}/git/blobs/{blob_sha}",
        )


    def get_commits(
        self,
        owner: str,
        repo: str,
    ) -> list:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        return self._request_json(
            "GET",
            f"/repos/{owner}/{repo}/commits",
        )


    def get_branches(
        self,
        owner: str,
        repo: str,
    ) -> list:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        return self._request_json(
            "GET",
            f"/repos/{owner}/{repo}/branches",
        )

    def get_pull_requests(
        self,
        owner: str,
        repo: str,
    ) -> list:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        return self._request_json(
            "GET",
            f"/repos/{owner}/{repo}/pulls",
        )


    def get_contributors(
        self,
        owner: str,
        repo: str,
    ) -> list:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        return self._request_json(
            "GET",
            f"/repos/{owner}/{repo}/contributors",
        )


    def get_releases(
        self,
        owner: str,
        repo: str,
    ) -> list:
        if not owner:
            raise ValueError("Repository owner cannot be empty")

        if not repo:
            raise ValueError("Repository name cannot be empty")

        return self._request_json(
            "GET",
            f"/repos/{owner}/{repo}/releases",
        )

    

    def search_repositories(
        self,
        query: str,
        page: int = 1,
        per_page: int = 30,
    ) -> dict:
        if not query or not query.strip():
            raise ValueError("Repository search query cannot be empty")

        return self._request_json(
            "GET",
            "/search/repositories",
            params={
                "q": query,
                "page": page,
                "per_page": per_page,
            },
        )


    def search_code(
        self,
        query: str,
        page: int = 1,
        per_page: int = 30,
    ) -> dict:
        if not query or not query.strip():
            raise ValueError("Code search query cannot be empty")

        return self._request_json(
            "GET",
            "/search/code",
            params={
                "q": query,
                "page": page,
                "per_page": per_page,
            },
        )



    def get_paginated(
        self,
        endpoint: str,
        params: dict | None = None,
        max_pages: int = 10,
    ) -> list:
        results = []
        params = params.copy() if params else {}

        for page in range(1, max_pages + 1):
            page_params = {
                **params,
                "page": page,
                "per_page": 100,
            }

            response = self._request(
                "GET",
                endpoint,
                params=page_params,
            )

            page_data = response.json()

            if not page_data:
                break

            results.extend(page_data)

            if len(page_data) < 100:
                break

        return results

