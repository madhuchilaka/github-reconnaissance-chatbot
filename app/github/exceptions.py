class GitHubAPIError(Exception):
    """Raised when the GitHub API returns an error response."""

    def __init__(
        self,
        status_code: int,
        message: str,
        retry_after: float | None = None,
    ):
        self.status_code = status_code
        self.retry_after = retry_after
        super().__init__(message)

    @property
    def is_retryable(self) -> bool:
        return self.status_code == 429 or self.status_code >= 500