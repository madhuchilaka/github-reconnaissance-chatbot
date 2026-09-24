from app.models.security_finding import SecurityFinding
from app.models.security_indicator import SecurityIndicator
from app.services.security_relationship_service import (
    build_security_relationship,
)


def analyze_security_relationship(
    finding: SecurityFinding,
    context: str,
    related_files: list[str],
):
    indicator = SecurityIndicator(
        indicator_type=finding.indicator_type,
        file_path=finding.file_path,
        evidence=finding.evidence,
    )

    return build_security_relationship(
        indicator=indicator,
        context=context,
        related_files=related_files,
        confidence=finding.confidence,
    )


def analyze_security_relationships(
    findings: list[SecurityFinding],
    context_by_file: dict[str, str],
    related_files_by_file: dict[str, list[str]],
):
    relationships = []

    for finding in findings:
        relationship = analyze_security_relationship(
            finding=finding,
            context=context_by_file.get(finding.file_path, ""),
            related_files=related_files_by_file.get(
                finding.file_path,
                [],
            ),
        )

        relationships.append(relationship)

    return relationships