from dataclasses import dataclass

from app.models.api_indicator import ApiIndicator
from app.models.domain_indicator import DomainIndicator
from app.models.file_indicator import FileIndicator
from app.models.security_finding import SecurityFinding
from app.models.technology_indicator import TechnologyIndicator


@dataclass(frozen=True)
class ReconAnalysisResult:
    files: list[FileIndicator]
    technologies: list[TechnologyIndicator]
    domains: list[DomainIndicator]
    apis: list[ApiIndicator]
    security_findings: list[SecurityFinding]