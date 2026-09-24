from dataclasses import dataclass


@dataclass(frozen=True)
class FileIndicator:
    name: str
    path: str
    extension: str | None
    category: str