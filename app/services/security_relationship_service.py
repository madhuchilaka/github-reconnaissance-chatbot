from app.models.security_indicator import SecurityIndicator
from app.models.security_relationship import SecurityRelationship


def build_security_relationship(
    indicator: SecurityIndicator,
    context: str,
    related_files: list[str],
    confidence: float,
) -> SecurityRelationship:
    return SecurityRelationship(
        indicator_type=indicator.indicator_type,
        file_path=indicator.file_path,
        context=context,
        related_files=tuple(related_files),
        confidence=confidence,
    )