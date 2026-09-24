from app.models.security_finding import SecurityFinding
from app.models.security_finding_record import SecurityFindingRecord


def create_security_finding_record(
    finding: SecurityFinding,
    finding_id: str,
) -> SecurityFindingRecord:
    return SecurityFindingRecord(
        finding_id=finding_id,
        indicator_type=finding.indicator_type,
        file_path=finding.file_path,
        evidence=finding.evidence,
        severity=finding.severity,
        confidence=finding.confidence,
        requires_review=finding.requires_review,
        status="open",
    )


def create_security_finding_records(
    findings: list[SecurityFinding],
    finding_ids: list[str],
) -> list[SecurityFindingRecord]:
    if len(findings) != len(finding_ids):
        raise ValueError(
            "findings and finding_ids must have the same length"
        )

    return [
        create_security_finding_record(
            finding=finding,
            finding_id=finding_id,
        )
        for finding, finding_id in zip(findings, finding_ids)
    ]