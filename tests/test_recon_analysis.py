from app.models.api_indicator import ApiIndicator
from app.models.domain_indicator import DomainIndicator
from app.models.file_indicator import FileIndicator
from app.models.recon_analysis import ReconAnalysisResult
from app.models.security_finding import SecurityFinding
from app.models.technology_indicator import TechnologyIndicator


def test_recon_analysis_result_stores_analysis_outputs():
    file_indicator = FileIndicator(
        name="main.py",
        path="main.py",
        extension=".py",
        category="source",
    )

    technology_indicator = TechnologyIndicator(
        name="Python",
        category="language",
        evidence=["main.py"],
    )

    domain_indicator = DomainIndicator(
        domain="example.com",
        evidence=["README.md"],
    )

    api_indicator = ApiIndicator(
        url="https://api.example.com/users",
        method="GET",
        evidence=["main.py"],
    )

    security_finding = SecurityFinding(
        indicator_type="GITHUB_TOKEN",
        file_path="config.py",
        evidence="ghp_********************",
        severity="high",
        confidence=0.95,
        requires_review=True,
    )

    result = ReconAnalysisResult(
        files=[file_indicator],
        technologies=[technology_indicator],
        domains=[domain_indicator],
        apis=[api_indicator],
        security_findings=[security_finding],
    )

    assert result.files == [file_indicator]
    assert result.technologies == [technology_indicator]
    assert result.domains == [domain_indicator]
    assert result.apis == [api_indicator]
    assert result.security_findings == [security_finding]