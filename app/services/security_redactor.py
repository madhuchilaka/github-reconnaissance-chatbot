from app.models.security_indicator import SecurityIndicator


def redact_secret(secret: str) -> str:
    if not secret:
        return ""

    if len(secret) <= 6:
        return "*" * len(secret)

    return secret[:4] + "*" * 20


def redact_security_indicator(
    indicator: SecurityIndicator,
) -> SecurityIndicator:
    return SecurityIndicator(
        indicator_type=indicator.indicator_type,
        file_path=indicator.file_path,
        evidence=redact_secret(indicator.evidence),
    )