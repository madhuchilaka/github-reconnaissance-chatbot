from dataclasses import asdict

from mcp.server.mcpserver import MCPServer

from app.github.client import GitHubClient
from app.tools.executor import ToolExecutor
from app.tools.validation import (
    validate_search_repositories_arguments,
    validate_search_code_arguments,
    validate_get_repository_arguments,
    validate_get_repository_contents_arguments,
    validate_get_file_arguments,
    validate_get_commits_arguments,
    validate_get_branches_arguments,
    validate_get_pull_requests_arguments,
    validate_get_contributors_arguments,
    validate_get_releases_arguments,
)
from app.services.recon_analysis_service import ReconAnalysisService
from app.services.repository_recon_service import RepositoryReconService


mcp = MCPServer("GitHub Reconnaissance Server")


@mcp.tool()
def get_repository(owner: str, repo: str) -> dict:
    """Get detailed metadata for a public GitHub repository."""
    arguments = {
        "owner": owner,
        "repo": repo,
    }

    validate_get_repository_arguments(arguments)

    client = GitHubClient()

    try:
        executor = ToolExecutor(client)

        return executor.get_repository(
            owner=owner,
            repo=repo,
        )
    finally:
        client.close()


@mcp.tool()
def search_repositories(
    query: str,
    page: int = 1,
    per_page: int = 30,
) -> dict:
    """Search public GitHub repositories."""
    arguments = {
        "query": query,
        "page": page,
        "per_page": per_page,
    }

    validate_search_repositories_arguments(arguments)

    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.search_repositories(
            query=query,
            page=page,
            per_page=per_page,
        )
    finally:
        client.close()


@mcp.tool()
def get_repository_contents(
    owner: str,
    repo: str,
    path: str = "",
) -> dict | list:
    """Get files or directories from a GitHub repository."""
    arguments = {
        "owner": owner,
        "repo": repo,
        "path": path,
    }

    validate_get_repository_contents_arguments(arguments)

    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.get_repository_contents(
            owner=owner,
            repo=repo,
            path=path,
        )
    finally:
        client.close()


@mcp.tool()
def search_code(
    query: str,
    page: int = 1,
    per_page: int = 30,
) -> dict:
    """Search code in public GitHub repositories."""
    arguments = {
        "query": query,
        "page": page,
        "per_page": per_page,
    }

    validate_search_code_arguments(arguments)

    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.search_code(
            query=query,
            page=page,
            per_page=per_page,
        )
    finally:
        client.close()


@mcp.tool()
def get_file(
    owner: str,
    repo: str,
    path: str,
) -> dict | list:
    """Get a file from a GitHub repository."""
    arguments = {
        "owner": owner,
        "repo": repo,
        "path": path,
    }

    validate_get_file_arguments(arguments)

    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.get_file(
            owner=owner,
            repo=repo,
            path=path,
        )
    finally:
        client.close()


@mcp.tool()
def get_commits(
    owner: str,
    repo: str,
) -> list:
    """Get commits from a GitHub repository."""
    arguments = {
        "owner": owner,
        "repo": repo,
    }

    validate_get_commits_arguments(arguments)

    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.get_commits(
            owner=owner,
            repo=repo,
        )
    finally:
        client.close()


@mcp.tool()
def get_branches(
    owner: str,
    repo: str,
) -> list:
    """Get branches from a GitHub repository."""
    arguments = {
        "owner": owner,
        "repo": repo,
    }

    validate_get_branches_arguments(arguments)
    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.get_branches(
            owner=owner,
            repo=repo,
        )
    finally:
        client.close()


@mcp.tool()
def get_pull_requests(
    owner: str,
    repo: str,
) -> list:
    """Get pull requests from a GitHub repository."""
    arguments = {
        "owner": owner,
        "repo": repo,
    }

    validate_get_pull_requests_arguments(arguments)

    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.get_pull_requests(
            owner=owner,
            repo=repo,
        )
    finally:
        client.close()


@mcp.tool()
def get_contributors(
    owner: str,
    repo: str,
) -> list:
    """Get contributors to a GitHub repository."""
    arguments = {
        "owner": owner,
        "repo": repo,
    }

    validate_get_contributors_arguments(arguments)
    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.get_contributors(
            owner=owner,
            repo=repo,
        )
    finally:
        client.close()


@mcp.tool()
def get_releases(
    owner: str,
    repo: str,
) -> list:
    """Get releases from a GitHub repository."""
    arguments = {
        "owner": owner,
        "repo": repo,
    }

    validate_get_releases_arguments(arguments)
    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        return executor.get_releases(
            owner=owner,
            repo=repo,
        )
    finally:
        client.close()


@mcp.tool()
def analyze_repository(owner: str, repo: str) -> dict:
    """
    Run reconnaissance analysis on a public GitHub repository.

    Analyze repository files and identify technologies, domains, APIs,
    and potential security findings that require human review.
    """
    arguments = {
        "owner": owner,
        "repo": repo,
    }

    validate_get_repository_arguments(arguments)

    client = GitHubClient()

    try:
        repository_recon_service = RepositoryReconService(client)
        recon_analysis_service = ReconAnalysisService(
            repository_recon_service
        )

        result = recon_analysis_service.analyze_repository(
            owner=owner,
            repo=repo,
        )

        return {
            "files": [asdict(item) for item in result.files],
            "technologies": [asdict(item) for item in result.technologies],
            "domains": [asdict(item) for item in result.domains],
            "apis": [asdict(item) for item in result.apis],
            "security_findings": [asdict(item) for item in result.security_findings],
        }
    finally:
        client.close()


if __name__ == "__main__":
    mcp.run()
