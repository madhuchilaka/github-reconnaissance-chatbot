from dataclasses import dataclass

from app.models.repository_metadata import RepositoryMetadata


@dataclass(frozen=True)
class RepositoryReconData:
    metadata: RepositoryMetadata
    contents: list[dict]
    branches: list[dict]
    commits: list[dict]
    pull_requests: list[dict]
    contributors: list[dict]
    releases: list[dict]
