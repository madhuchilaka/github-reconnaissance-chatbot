from app.api.schemas import ReconAnalysisRequest
from app.models.api_indicator import ApiIndicator
from app.models.domain_indicator import DomainIndicator
from app.models.file_indicator import FileIndicator
from app.models.recon_analysis import ReconAnalysisResult
from app.models.security_finding import SecurityFinding
from app.models.technology_indicator import TechnologyIndicator

from app.api.schemas import ReconAnalysisRequest, ReconAnalysisResponse



def test_recon_analysis_request_accepts_owner_and_repo():
    request = ReconAnalysisRequest(
        owner="microsoft",
        repo="vscode",
    )

    assert request.owner == "microsoft"
    assert request.repo == "vscode"



def test_recon_analysis_response_accepts_empty_results():
    response = ReconAnalysisResponse(
        files=[],
        technologies=[],
        domains=[],
        apis=[],
        security_findings=[],
    )

    assert response.files == []
    assert response.technologies == []
    assert response.domains == []
    assert response.apis == []
    assert response.security_findings == []







def test_recon_analysis_response_serializes_domain_result():
    result = ReconAnalysisResult(
        files=[
            FileIndicator(
                name="main.py",
                path="main.py",
                extension=".py",
                category="source",
            )
        ],
        technologies=[
            TechnologyIndicator(
                name="Python",
                category="language",
                evidence=["main.py"],
            )
        ],
        domains=[
            DomainIndicator(
                domain="example.com",
                evidence=["main.py"],
            )
        ],
        apis=[
            ApiIndicator(
                url="https://api.example.com/users",
                method="GET",
                evidence=["main.py"],
            )
        ],
        security_findings=[
            SecurityFinding(
                indicator_type="GITHUB_TOKEN",
                file_path=".env",
                evidence="ghp_********************",
                severity="high",
                confidence=0.95,
                requires_review=True,
            )
        ],
    )

    response = ReconAnalysisResponse.model_validate(result, from_attributes=True)

    assert response.files[0].path == "main.py"
    assert response.technologies[0].name == "Python"
    assert response.domains[0].domain == "example.com"
    assert response.apis[0].url == "https://api.example.com/users"
    assert response.security_findings[0].severity == "high"