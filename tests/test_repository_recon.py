from app.models.repository import RepositoryCandidate
from app.models.repository_metadata import RepositoryMetadata
from app.models.repository_recon import RepositoryReconData


def test_repository_recon_data():
    metadata = RepositoryMetadata(
        id=1,
        full_name="example/project",
        owner_login="example",
        html_url="https://github.com/example/project",
        description="Example project",
        default_branch="main",
        visibility="public",
        language="Python",
        topics=[],
        fork=False,
        archived=False,
        stargazers_count=10,
        forks_count=2,
        open_issues_count=1,
        created_at=None,
        updated_at=None,
        pushed_at=None,
    )

    recon = RepositoryReconData(
        metadata=metadata,
        contents=[],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    assert recon.metadata == metadata
    assert recon.contents == []
    assert recon.branches == []
    assert recon.commits == []
    assert recon.pull_requests == []
    assert recon.contributors == []
    assert recon.releases == []
