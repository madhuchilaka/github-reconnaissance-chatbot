from app.models.security_finding import SecurityFinding
from app.models.security_indicator import SecurityIndicator
from app.services.security_redactor import redact_security_indicator
from app.services.security_classifier import classify_security_indicator


def build_security_finding(
    indicator: SecurityIndicator,
    severity: str | None = None,
    confidence: float | None = None,
    requires_review: bool | None = None,
) -> SecurityFinding:
    redacted_indicator = redact_security_indicator(indicator)

    classification = classify_security_indicator(indicator)

    return SecurityFinding(
        indicator_type=redacted_indicator.indicator_type,
        file_path=redacted_indicator.file_path,
        evidence=redacted_indicator.evidence,
        severity=severity if severity is not None else classification["severity"],
        confidence=(
            confidence
            if confidence is not None
            else classification["confidence"]
        ),
        requires_review=(
            requires_review
            if requires_review is not None
            else classification["requires_review"]
        ),
    )


def build_security_findings(
    indicators: list[SecurityIndicator],
) -> list[SecurityFinding]:
    return [
        build_security_finding(indicator)
        for indicator in indicators
    ]