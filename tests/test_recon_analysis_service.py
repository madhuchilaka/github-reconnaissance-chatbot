from unittest.mock import Mock
import base64

from app.services.recon_analysis_service import ReconAnalysisService
from app.models.repository_recon import RepositoryReconData
from app.services.recon_analysis_service import ReconAnalysisService


def test_load_file_contents_decodes_repository_files():
    repository_recon_service = Mock()

    repository_recon_service.load_file.side_effect = [
        {
            "path": "main.py",
            "content": base64.b64encode(
                b"print('hello')"
            ).decode("ascii"),
            "encoding": "base64",
        },
        {
            "path": "README.md",
            "content": base64.b64encode(
                b"# Example"
            ).decode("ascii"),
            "encoding": "base64",
        },
    ]

    service = ReconAnalysisService(repository_recon_service)

    files = [
        {"path": "main.py"},
        {"path": "README.md"},
    ]

    result = service.load_file_contents(
        owner="example",
        repo="project",
        files=files,
    )

    assert result == [
        {
            "path": "main.py",
            "content": "print('hello')",
        },
        {
            "path": "README.md",
            "content": "# Example",
        },
    ]

    assert repository_recon_service.load_file.call_count == 2





def test_extract_file_indicators():
    repository_recon_service = Mock()
    service = ReconAnalysisService(repository_recon_service)

    recon_data = RepositoryReconData(
        metadata=Mock(),
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
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    result = service.extract_file_indicators(recon_data)

    assert len(result) == 2
    assert result[0].name == "main.py"
    assert result[0].category == "source"
    assert result[1].name == "Dockerfile"
    assert result[1].category == "container"



def test_extract_domain_indicators():
    repository_recon_service = Mock()
    service = ReconAnalysisService(repository_recon_service)

    recon_data = RepositoryReconData(
        metadata=Mock(),
        contents=[
            {
                "name": "config.py",
                "path": "config.py",
                "type": "file",
                "content": "API_URL = 'https://api.example.com'",
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    result = service.extract_domain_indicators(recon_data)

    assert len(result) == 1
    assert result[0].domain == "api.example.com"
    assert result[0].evidence == ["config.py"]



def test_extract_api_indicators():
    repository_recon_service = Mock()
    service = ReconAnalysisService(repository_recon_service)

    recon_data = RepositoryReconData(
        metadata=Mock(),
        contents=[
            {
                "name": "client.py",
                "path": "client.py",
                "type": "file",
                "content": (
                    "response = requests.get("
                    "https://api.example.com/users"
                    ")"
                ),
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    result = service.extract_api_indicators(recon_data)

    assert len(result) == 1
    assert result[0].url == "https://api.example.com/users"
    assert result[0].method == "GET"
    assert result[0].evidence == ["client.py"]


def test_analyze_security():
    repository_recon_service = Mock()
    service = ReconAnalysisService(repository_recon_service)

    files = [
        {
            "path": "config/github.py",
            "content": "token = 'ghp_1234567890abcdefghijklmnopqrstuvwxyz'",
        },
    ]

    result = service.analyze_security(files)

    assert len(result) == 1
    assert result[0].indicator_type == "GITHUB_TOKEN"
    assert result[0].file_path == "config/github.py"
    assert result[0].evidence == "ghp_********************"
    assert result[0].severity == "high"
    assert result[0].confidence == 0.95
    assert result[0].requires_review is True



def test_extract_technology_indicators():
    repository_recon_service = Mock()

    service = ReconAnalysisService(repository_recon_service)

    recon_data = RepositoryReconData(
        metadata=Mock(),
        contents=[
            {
                "name": "main.py",
                "path": "main.py",
                "type": "file",
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    result = service.extract_technology_indicators(
        recon_data,
        owner="example",
        repo="project",
    )

    assert len(result) == 1
    assert result[0].name == "Python"
    assert result[0].category == "language"
    assert result[0].evidence == ["main.py"]


def test_analyze_repository_combines_all_analysis_outputs():
    repository_recon_service = Mock()

    recon_data = RepositoryReconData(
        metadata=Mock(),
        contents=[
            {
                "name": "main.py",
                "path": "main.py",
                "type": "file",
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    repository_recon_service.collect_repository_for_analysis.return_value = recon_data

    repository_recon_service.load_file.return_value = {
        "path": "main.py",
        "content": "cHJpbnQoJ2hlbGxvJyk=",
        "encoding": "base64",
    }

    service = ReconAnalysisService(repository_recon_service)

    result = service.analyze_repository(
        owner="example",
        repo="project",
    )

    assert len(result.files) == 1
    assert result.files[0].name == "main.py"

    assert len(result.technologies) == 1
    assert result.technologies[0].name == "Python"

    assert result.domains == []
    assert result.apis == []
    assert result.security_findings == []

    repository_recon_service.collect_repository_for_analysis.assert_called_once_with(
        "example",
        "project",
    )

    repository_recon_service.load_file.assert_called_once_with(
        "example",
        "project",
        "main.py",
    )