from app.database.connection import get_connection


def initialize_database() -> None:
    connection = get_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS security_findings (
                finding_id TEXT PRIMARY KEY,
                indicator_type TEXT NOT NULL,
                file_path TEXT NOT NULL,
                evidence TEXT NOT NULL,
                severity TEXT NOT NULL,
                confidence REAL NOT NULL,
                requires_review INTEGER NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        connection.commit()
    finally:
        connection.close()