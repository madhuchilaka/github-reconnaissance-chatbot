from app.database.connection import get_connection
from app.models.security_finding_record import SecurityFindingRecord


class SecurityFindingRepository:

    def create(
        self,
        record: SecurityFindingRecord,
    ) -> SecurityFindingRecord:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO security_findings (
                    finding_id,
                    indicator_type,
                    file_path,
                    evidence,
                    severity,
                    confidence,
                    requires_review,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.finding_id,
                    record.indicator_type,
                    record.file_path,
                    record.evidence,
                    record.severity,
                    record.confidence,
                    int(record.requires_review),
                    record.status,
                ),
            )
            connection.commit()
            return record
        finally:
            connection.close()


    def get_by_id(
        self,
        finding_id: str,
    ) -> SecurityFindingRecord | None:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    finding_id,
                    indicator_type,
                    file_path,
                    evidence,
                    severity,
                    confidence,
                    requires_review,
                    status
                FROM security_findings
                WHERE finding_id = ?
                """,
                (finding_id,),
            ).fetchone()

            if row is None:
                return None

            return SecurityFindingRecord(
                finding_id=row["finding_id"],
                indicator_type=row["indicator_type"],
                file_path=row["file_path"],
                evidence=row["evidence"],
                severity=row["severity"],
                confidence=row["confidence"],
                requires_review=bool(row["requires_review"]),
                status=row["status"],
            )
        finally:
            connection.close()


    def get_all(self) -> list[SecurityFindingRecord]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    finding_id,
                    indicator_type,
                    file_path,
                    evidence,
                    severity,
                    confidence,
                    requires_review,
                    status
                FROM security_findings
                ORDER BY rowid
                """
            ).fetchall()

            return [
                SecurityFindingRecord(
                    finding_id=row["finding_id"],
                    indicator_type=row["indicator_type"],
                    file_path=row["file_path"],
                    evidence=row["evidence"],
                    severity=row["severity"],
                    confidence=row["confidence"],
                    requires_review=bool(row["requires_review"]),
                    status=row["status"],
                )
                for row in rows
            ]
        finally:
            connection.close()



    def update(
        self,
        record: SecurityFindingRecord,
    ) -> SecurityFindingRecord:
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE security_findings
                SET
                    indicator_type = ?,
                    file_path = ?,
                    evidence = ?,
                    severity = ?,
                    confidence = ?,
                    requires_review = ?,
                    status = ?
                WHERE finding_id = ?
                """,
                (
                    record.indicator_type,
                    record.file_path,
                    record.evidence,
                    record.severity,
                    record.confidence,
                    int(record.requires_review),
                    record.status,
                    record.finding_id,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Security finding not found: {record.finding_id}"
                )

            connection.commit()
            return record
        finally:
            connection.close()