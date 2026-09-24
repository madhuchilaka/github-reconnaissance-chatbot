from fastapi import FastAPI

from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    ReconAnalysisRequest,
    ReconAnalysisResponse,
    ToolRequest,
)
from app.github.client import GitHubClient
from app.services.recon_analysis_service import ReconAnalysisService
from app.services.repository_recon_service import RepositoryReconService
from app.tools.dispatcher import ToolDispatcher
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.ai.agent import AIAgent
from app.ai.client import AIClient
from app.mcp.client import MCPClient
from app.mcp.runtime import MCPRuntime


app = FastAPI(
    title="AI-Powered GitHub Reconnaissance API",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "github-recon-api",
    }


@app.post("/tools/execute")
def execute_tool(request: ToolRequest) -> dict:
    client = GitHubClient()

    try:
        executor = ToolExecutor(client)
        registry = ToolRegistry()
        dispatcher = ToolDispatcher(executor, registry)

        result = dispatcher.dispatch(
            request.tool_name,
            request.arguments,
        )

        return {
            "tool_name": result.tool_name,
            "success": result.success,
            "data": result.data,
            "error": result.error,
        }
    finally:
        client.close()


@app.post("/recon/analyze", response_model=ReconAnalysisResponse)
def recon_analysis(
    request: ReconAnalysisRequest,
) -> ReconAnalysisResponse:
    client = GitHubClient()

    try:
        repository_recon_service = RepositoryReconService(client)
        recon_analysis_service = ReconAnalysisService(
            repository_recon_service
        )

        result = recon_analysis_service.analyze_repository(
            request.owner,
            request.repo,
        )

        return ReconAnalysisResponse.model_validate(
            result,
            from_attributes=True,
        )
    finally:
        client.close()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    ai_client = AIClient()
    mcp_runtime = MCPRuntime(MCPClient())

    agent = AIAgent(
        ai_client,
        mcp_runtime,
    )

    result = agent.respond(request.message)

    return ChatResponse(response=result)