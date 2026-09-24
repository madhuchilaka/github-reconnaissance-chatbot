from app.models.security_finding import SecurityFinding
from app.services.security_extractor import extract_security_indicators
from app.services.security_finding_service import build_security_findings


def analyze_security(
    files: list[dict],
) -> list[SecurityFinding]:
    indicators = extract_security_indicators(files)

    return build_security_findings(indicators)