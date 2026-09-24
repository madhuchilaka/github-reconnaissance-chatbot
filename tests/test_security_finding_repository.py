import pytest

from app.database.security_finding_repository import SecurityFindingRepository
from app.database.schema import initialize_database
from app.models.security_finding_record import SecurityFindingRecord


def test_create_security_finding_record(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    from app.database import connection

    monkeypatch.setattr(
        connection,
        "DATABASE_PATH",
        str(database_path),
    )

    initialize_database()

    repository = SecurityFindingRepository()

    record = SecurityFindingRecord(
        finding_id="finding-001",
        indicator_type="GITHUB_TOKEN",
        file_path=".env",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
        status="open",
    )

    created = repository.create(record)

    assert created == record

    database_connection = connection.get_connection()
    row = database_connection.execute(
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
        (record.finding_id,),
    ).fetchone()
    database_connection.close()

    assert row is not None
    assert dict(row) == {
        "finding_id": "finding-001",
        "indicator_type": "GITHUB_TOKEN",
        "file_path": ".env",
        "evidence": "ghp_********************",
        "severity": "high",
        "confidence": 0.95,
        "requires_review": 1,
        "status": "open",
    }

    fetched = repository.get_by_id("finding-001")

    assert fetched == record



def test_get_by_id_returns_none_for_missing_finding(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    from app.database import connection

    monkeypatch.setattr(
        connection,
        "DATABASE_PATH",
        str(database_path),
    )

    initialize_database()

    repository = SecurityFindingRepository()

    result = repository.get_by_id("missing-finding")

    assert result is None




def test_get_all_returns_all_findings(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    from app.database import connection

    monkeypatch.setattr(
        connection,
        "DATABASE_PATH",
        str(database_path),
    )

    initialize_database()

    repository = SecurityFindingRepository()

    first_record = SecurityFindingRecord(
        finding_id="finding-001",
        indicator_type="GITHUB_TOKEN",
        file_path=".env",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
        status="open",
    )

    second_record = SecurityFindingRecord(
        finding_id="finding-002",
        indicator_type="AWS_ACCESS_KEY",
        file_path="config.py",
        evidence="AKIA********************",
        severity="critical",
        confidence=0.98,
        requires_review=True,
        status="open",
    )

    repository.create(first_record)
    repository.create(second_record)

    findings = repository.get_all()

    assert findings == [first_record, second_record]




def test_update_security_finding_record(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    from app.database import connection

    monkeypatch.setattr(
        connection,
        "DATABASE_PATH",
        str(database_path),
    )

    initialize_database()

    repository = SecurityFindingRepository()

    original_record = SecurityFindingRecord(
        finding_id="finding-001",
        indicator_type="GITHUB_TOKEN",
        file_path=".env",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
        status="open",
    )

    repository.create(original_record)

    updated_record = SecurityFindingRecord(
        finding_id="finding-001",
        indicator_type="GITHUB_TOKEN",
        file_path=".env",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
        status="reviewed",
    )

    result = repository.update(updated_record)

    assert result == updated_record
    assert repository.get_by_id("finding-001") == updated_record




def test_update_missing_security_finding_record_raises(
    tmp_path,
    monkeypatch,
):
    database_path = tmp_path / "test.db"

    from app.database import connection

    monkeypatch.setattr(
        connection,
        "DATABASE_PATH",
        str(database_path),
    )

    initialize_database()

    repository = SecurityFindingRepository()

    record = SecurityFindingRecord(
        finding_id="missing-finding",
        indicator_type="GITHUB_TOKEN",
        file_path=".env",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
        status="reviewed",
    )

    with pytest.raises(
        ValueError,
        match="Security finding not found: missing-finding",
    ):
        repository.update(record)