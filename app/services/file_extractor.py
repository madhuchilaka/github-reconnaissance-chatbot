from pathlib import Path
from app.models.file_indicator import FileIndicator
from app.models.repository_recon import RepositoryReconData

def extract_extension(filename: str) -> str | None:
    suffix = Path(filename).suffix.lower()

    if not suffix:
        return None

    return suffix

def classify_file(filename: str) -> str:
    name = filename.lower()
    extension = extract_extension(name)

    if name == "dockerfile":
        return "container"

    if extension in {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".c",
        ".cpp",
        ".cs",
        ".go",
        ".rs",
        ".php",
        ".rb",
        ".swift",
        ".kt",
    }:
        return "source"

    if extension in {
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".cfg",
        ".conf",
        ".env",
    }:
        return "configuration"

    if extension in {
        ".md",
        ".rst",
        ".txt",
    }:
        return "documentation"

    return "other"



def extract_file_indicator(file_data: dict) -> FileIndicator:
    name = file_data["name"]
    path = file_data["path"]

    return FileIndicator(
        name=name,
        path=path,
        extension=extract_extension(name),
        category=classify_file(name),
    )


def extract_file_indicators(
    files: list[dict],
) -> list[FileIndicator]:
    return [
        extract_file_indicator(file_data)
        for file_data in files
    ]


def extract_repository_files(
    recon_data: RepositoryReconData,
) -> list[FileIndicator]:
    return extract_file_indicators(recon_data.contents)