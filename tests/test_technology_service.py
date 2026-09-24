from unittest.mock import Mock

from app.models.repository_recon import RepositoryReconData
from app.models.repository_metadata import RepositoryMetadata
from app.models.technology_indicator import TechnologyIndicator
from app.services.technology_service import TechnologyService
from app.services.repository_recon_service import RepositoryReconService


def test_extract_technologies_from_repository_files():
    metadata = Mock(spec=RepositoryMetadata)

    recon_data = RepositoryReconData(
        metadata=metadata,
        contents=[
            {
                "name": "main.py",
                "path": "main.py",
                "type": "file",
            },
            {
                "name": "Dockerfile",
                "path": "Dockerfile",
                "type": "file",
            },
            {
                "name": "package.json",
                "path": "package.json",
                "type": "file",
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    service = TechnologyService()

    result = service.extract_technologies(recon_data)

    assert result == [
        TechnologyIndicator(
            name="Python",
            category="language",
            evidence=["main.py"],
        ),
        TechnologyIndicator(
            name="Docker",
            category="container",
            evidence=["Dockerfile"],
        ),
        TechnologyIndicator(
            name="Node.js",
            category="runtime",
            evidence=["package.json"],
        ),
    ]


def test_extract_technologies_from_package_json():
    metadata = Mock(spec=RepositoryMetadata)

    recon_data = RepositoryReconData(
        metadata=metadata,
        contents=[
            {
                "name": "package.json",
                "path": "package.json",
                "type": "file",
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    package_data = {
        "dependencies": {
            "react": "^19.0.0",
            "express": "^5.0.0",
        }
    }

    def file_loader(owner: str, repo: str, path: str) -> dict:
        assert owner == "example"
        assert repo == "project"
        assert path == "package.json"

        return {
            "content": "unused",
            "encoding": "base64",
        }

    service = TechnologyService(
        file_loader=file_loader,
        owner="example",
        repo="project",
    )

    service.parse_package_data = Mock(return_value=package_data)

    result = service.extract_technologies(recon_data)

    assert result == [
        TechnologyIndicator(
            name="Node.js",
            category="runtime",
            evidence=["package.json"],
        ),
        TechnologyIndicator(
            name="React",
            category="framework",
            evidence=["package.json"],
        ),
        TechnologyIndicator(
            name="Express",
            category="framework",
            evidence=["package.json"],
        ),
    ]


def test_extract_technologies_using_repository_recon_service():
    metadata = Mock(spec=RepositoryMetadata)

    recon_data = RepositoryReconData(
        metadata=metadata,
        contents=[
            {
                "name": "package.json",
                "path": "package.json",
                "type": "file",
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    client = Mock()

    client.get_file.return_value = {
        "name": "package.json",
        "path": "package.json",
        "type": "file",
        "content": "eyJkZXBlbmRlbmNpZXMiOiB7InJlYWN0IjogIl4xOS4wLjAiLCAiZXhwcmVzcyI6ICJeNS4wLjAifX0=",
        "encoding": "base64",
    }

    repository_recon_service = RepositoryReconService(client)

    technology_service = TechnologyService(
        file_loader=repository_recon_service.load_file,
        owner="example",
        repo="project",
    )

    result = technology_service.extract_technologies(recon_data)

    assert result == [
        TechnologyIndicator(
            name="Node.js",
            category="runtime",
            evidence=["package.json"],
        ),
        TechnologyIndicator(
            name="React",
            category="framework",
            evidence=["package.json"],
        ),
        TechnologyIndicator(
            name="Express",
            category="framework",
            evidence=["package.json"],
        ),
    ]

    client.get_file.assert_called_once_with(
        "example",
        "project",
        "package.json",
    )