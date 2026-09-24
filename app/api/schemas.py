from typing import Any

from pydantic import BaseModel


class ToolRequest(BaseModel):
    tool_name: str
    arguments: dict[str, Any]


class ReconAnalysisRequest(BaseModel):
    owner: str
    repo: str


class FileIndicatorResponse(BaseModel):
    name: str
    path: str
    extension: str | None
    category: str


class TechnologyIndicatorResponse(BaseModel):
    name: str
    category: str
    evidence: list[str]


class DomainIndicatorResponse(BaseModel):
    domain: str
    evidence: list[str]


class ApiIndicatorResponse(BaseModel):
    url: str
    method: str | None
    evidence: list[str]


class SecurityFindingResponse(BaseModel):
    indicator_type: str
    file_path: str
    evidence: str
    severity: str
    confidence: float
    requires_review: bool


class ReconAnalysisResponse(BaseModel):
    files: list[FileIndicatorResponse]
    technologies: list[TechnologyIndicatorResponse]
    domains: list[DomainIndicatorResponse]
    apis: list[ApiIndicatorResponse]
    security_findings: list[SecurityFindingResponse]


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str