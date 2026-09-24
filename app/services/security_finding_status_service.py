from app.models.security_finding_record import SecurityFindingRecord


ALLOWED_TRANSITIONS = {
    "open": {"reviewed"},
    "reviewed": {"resolved", "false_positive"},
    "resolved": set(),
    "false_positive": set(),
}


def update_finding_status(
    record: SecurityFindingRecord,
    new_status: str,
) -> SecurityFindingRecord:
    allowed_statuses = ALLOWED_TRANSITIONS.get(record.status)

    if allowed_statuses is None:
        raise ValueError(f"Unknown current status: {record.status}")

    if new_status not in allowed_statuses:
        raise ValueError(
            f"Invalid status transition: "
            f"{record.status} -> {new_status}"
        )

    return SecurityFindingRecord(
        finding_id=record.finding_id,
        indicator_type=record.indicator_type,
        file_path=record.file_path,
        evidence=record.evidence,
        severity=record.severity,
        confidence=record.confidence,
        requires_review=record.requires_review,
        status=new_status,
    )


def update_finding_statuses(
    records: list[SecurityFindingRecord],
    status_by_finding_id: dict[str, str],
) -> list[SecurityFindingRecord]:
    updated_records = []

    for record in records:
        new_status = status_by_finding_id.get(record.finding_id)

        if new_status is None:
            updated_records.append(record)
            continue

        updated_records.append(
            update_finding_status(
                record=record,
                new_status=new_status,
            )
        )

    return updated_records