from app.models.file_indicator import FileIndicator
from app.services.file_extractor import extract_extension
from app.services.file_extractor import (
    classify_file,
    extract_extension,
    extract_file_indicator,
    extract_file_indicators,
    extract_repository_files,
)
from app.models.repository_recon import RepositoryReconData


def test_file_indicator():
    indicator = FileIndicator(
        name="main.py",
        path="app/main.py",
        extension=".py",
        category="source",
    )

    assert indicator.name == "main.py"
    assert indicator.path == "app/main.py"
    assert indicator.extension == ".py"
    assert indicator.category == "source"


def test_extract_extension():
    assert extract_extension("main.py") == ".py"
    assert extract_extension("app.JS") == ".js"
    assert extract_extension("package.json") == ".json"


def test_extract_extension_without_extension():
    assert extract_extension("Dockerfile") is None

def test_classify_file():
    assert classify_file("main.py") == "source"
    assert classify_file("package.json") == "configuration"
    assert classify_file("README.md") == "documentation"
    assert classify_file("Dockerfile") == "container"
    assert classify_file("unknown.xyz") == "other"



def test_extract_file_indicator():
    result = extract_file_indicator(
        {
            "name": "main.py",
            "path": "app/main.py",
            "type": "file",
        }
    )

    assert result.name == "main.py"
    assert result.path == "app/main.py"
    assert result.extension == ".py"
    assert result.category == "source"



def test_extract_file_indicators():
    result = extract_file_indicators(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            },
            {
                "name": "README.md",
                "path": "README.md",
                "type": "file",
            },
        ]
    )

    assert result == [
        FileIndicator(
            name="main.py",
            path="app/main.py",
            extension=".py",
            category="source",
        ),
        FileIndicator(
            name="README.md",
            path="README.md",
            extension=".md",
            category="documentation",
        ),
    ]


def test_extract_repository_files():
    recon_data = RepositoryReconData(
        metadata=None,
        contents=[
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            },
            {
                "name": "README.md",
                "path": "README.md",
                "type": "file",
            },
        ],
        branches=[],
        commits=[],
        pull_requests=[],
        contributors=[],
        releases=[],
    )

    result = extract_repository_files(recon_data)

    assert result == [
        FileIndicator(
            name="main.py",
            path="app/main.py",
            extension=".py",
            category="source",
        ),
        FileIndicator(
            name="README.md",
            path="README.md",
            extension=".md",
            category="documentation",
        ),
    ]


def test_extract_file_indicator_for_dockerfile():
    result = extract_file_indicator(
        {
            "name": "Dockerfile",
            "path": "Dockerfile",
            "type": "file",
        }
    )

    assert result == FileIndicator(
        name="Dockerfile",
        path="Dockerfile",
        extension=None,
        category="container",
    )