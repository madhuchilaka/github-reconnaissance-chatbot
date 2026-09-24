from app.models.domain_indicator import DomainIndicator
from app.models.repository_recon import RepositoryReconData
from app.services.domain_extractor import (
    extract_domains,
    extract_repository_domains,
)

def test_extract_domains_from_url():
    files = [
        {
            "path": "config/settings.py",
            "content": "API_URL = 'https://api.example.com/v1'",
        }
    ]

    result = extract_domains(files)

    assert result == [
        DomainIndicator(
            domain="api.example.com",
            evidence=["config/settings.py"],
        )
    ]


def test_extract_subdomain():
    files = [
        {
            "path": "config/app.env",
            "content": "SERVICE_URL=https://payments.example.com",
        }
    ]

    result = extract_domains(files)

    assert result == [
        DomainIndicator(
            domain="payments.example.com",
            evidence=["config/app.env"],
        )
    ]


def test_extract_domains_without_domain():
    files = [
        {
            "path": "app/main.py",
            "content": "print('Hello World')",
        }
    ]

    result = extract_domains(files)

    assert result == []


def test_extract_domains_preserves_evidence_path():
    files = [
        {
            "path": "config/api.py",
            "content": "BASE_URL = 'https://api.example.com'",
        },
        {
            "path": "README.md",
            "content": "Visit https://api.example.com for the API.",
        },
    ]

    result = extract_domains(files)

    assert result == [
        DomainIndicator(
            domain="api.example.com",
            evidence=[
                "config/api.py",
                "README.md",
            ],
        )
    ]


def test_extract_repository_domains():
    recon_data = RepositoryReconData(
        metadata=None,
        contents=[
            {
                "path": "config/api.py",
                "content": "BASE_URL = 'https://api.example.com'",
            },
            {
                "path": "README.md",
                "content": "Visit https://api.example.com",
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    result = extract_repository_domains(recon_data)

    assert result == [
        DomainIndicator(
            domain="api.example.com",
            evidence=[
                "config/api.py",
                "README.md",
            ],
        )
    ]


def test_extract_domain_without_url_scheme():
    files = [
        {
            "path": "config/services.yaml",
            "content": "backend: api.example.com",
        }
    ]

    result = extract_domains(files)

    assert result == [
        DomainIndicator(
            domain="api.example.com",
            evidence=["config/services.yaml"],
        )
    ]



def test_extract_multiple_domains_from_same_file():
    files = [
        {
            "path": "config/services.yaml",
            "content": """
                backend: api.example.com
                payments: payments.example.com
            """,
        }
    ]

    result = extract_domains(files)

    assert result == [
        DomainIndicator(
            domain="api.example.com",
            evidence=["config/services.yaml"],
        ),
        DomainIndicator(
            domain="payments.example.com",
            evidence=["config/services.yaml"],
        ),
    ]