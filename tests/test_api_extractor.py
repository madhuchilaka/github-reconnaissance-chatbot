from app.services.api_extractor import extract_apis


def test_extract_api_url():
    files = [
        {
            "path": "src/client.py",
            "content": 'response = requests.get("https://api.example.com/users")',
        }
    ]

    results = extract_apis(files)

    assert len(results) == 1
    assert results[0].url == "https://api.example.com/users"
    assert results[0].evidence == ["src/client.py"]


def test_extract_api_url_without_scheme():
    files = [
        {
            "path": "src/config.js",
            "content": 'const API_URL = "api.example.com/v1/users"',
        }
    ]

    results = extract_apis(files)

    assert len(results) == 1
    assert results[0].url == "api.example.com/v1/users"
    assert results[0].evidence == ["src/config.js"]
from app.services.api_extractor import extract_apis


def test_extract_api_duplicate_url_with_multiple_evidence_files():
    files = [
        {
            "path": "src/client.py",
            "content": 'requests.get("https://api.example.com/users")',
        },
        {
            "path": "src/service.py",
            "content": 'requests.post("https://api.example.com/users")',
        },
    ]

    results = extract_apis(files)

    assert len(results) == 1
    assert results[0].url == "https://api.example.com/users"
    assert results[0].evidence == ["src/client.py", "src/service.py"]
def test_extract_api_http_method():
    files = [
        {
            "path": "src/client.py",
            "content": 'requests.get("https://api.example.com/users")',
        },
        {
            "path": "src/create.py",
            "content": 'requests.post("https://api.example.com/users")',
        },
    ]

    results = extract_apis(files)

    assert len(results) == 1

    assert results[0].url == "https://api.example.com/users"
    assert results[0].method == "GET"
def test_extract_multiple_api_urls_with_methods():
    files = [
        {
            "path": "src/client.py",
            "content": (
                'users = requests.get("https://api.example.com/users")\n'
                'orders = requests.post("https://api.example.com/orders")'
            ),
        }
    ]

    results = extract_apis(files)

    assert len(results) == 2

    assert results[0].url == "https://api.example.com/users"
    assert results[0].method == "GET"

    assert results[1].url == "https://api.example.com/orders"
    assert results[1].method == "POST"
from app.models.repository_metadata import RepositoryMetadata
from app.models.repository_recon import RepositoryReconData
from app.services.api_extractor import extract_repository_apis


def test_extract_repository_apis():
    metadata = RepositoryMetadata(
        id=1,
        full_name="example/demo",
        owner_login="example",
        html_url="https://github.com/example/demo",
        description=None,
        default_branch="main",
        visibility="public",
        language="Python",
        topics=[],
        fork=False,
        archived=False,
        stargazers_count=0,
        forks_count=0,
        open_issues_count=0,
        created_at=None,
        updated_at=None,
        pushed_at=None,
    )

    recon_data = RepositoryReconData(
        metadata=metadata,
        contents=[
            {
                "path": "src/client.py",
                "content": 'requests.get("https://api.example.com/users")',
            }
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    results = extract_repository_apis(recon_data)

    assert len(results) == 1
    assert results[0].url == "https://api.example.com/users"
    assert results[0].method == "GET"
    assert results[0].evidence == ["src/client.py"]

def test_extract_apis_with_no_api_urls():
    files = [
        {
            "path": "README.md",
            "content": "This is a documentation file with no API endpoint.",
        },
        {
            "path": "src/main.py",
            "content": "print('Hello World')",
        },
    ]

    results = extract_apis(files)

    assert results == []
