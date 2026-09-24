from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityRelationship:
    indicator_type: str
    file_path: str
    context: str
    related_files: tuple[str, ...]
    confidence: float