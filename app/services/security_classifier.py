from app.models.security_indicator import SecurityIndicator


CLASSIFICATION_RULES = {
    "GITHUB_TOKEN": {
        "severity": "high",
        "confidence": 0.95,
    },
    "GITHUB_FINE_GRAINED_TOKEN": {
        "severity": "high",
        "confidence": 0.95,
    },
    "AWS_ACCESS_KEY": {
        "severity": "critical",
        "confidence": 0.98,
    },
    "AWS_SECRET_KEY": {
        "severity": "critical",
        "confidence": 0.98,
    },
}


def classify_security_indicator(
    indicator: SecurityIndicator,
) -> dict:
    classification = CLASSIFICATION_RULES.get(
        indicator.indicator_type,
        {
            "severity": "medium",
            "confidence": 0.70,
        },
    )

    return {
        "severity": classification["severity"],
        "confidence": classification["confidence"],
        "requires_review": True,
    }