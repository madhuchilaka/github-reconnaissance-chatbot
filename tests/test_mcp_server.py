import asyncio
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.models.api_indicator import ApiIndicator
from app.models.domain_indicator import DomainIndicator
from app.models.file_indicator import FileIndicator
from app.models.security_finding import SecurityFinding
from app.models.technology_indicator import TechnologyIndicator


async def run_mcp_test():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("Available MCP tools:")

            for tool in tools.tools:
                print("-", tool.name)

            result = await session.call_tool(
                "get_repository",
                {
                    "owner": "microsoft",
                    "repo": "vscode",
                },
            )

            print("Tool result:")
            print(result)


def test_mcp_exposes_all_github_tools():
    async def check_tools():
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.server"],
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                await session.initialize()

                result = await session.list_tools()

                return {tool.name for tool in result.tools}

    tool_names = asyncio.run(check_tools())

    expected_tools = {
        "search_repositories",
        "get_repository",
        "get_repository_contents",
        "search_code",
        "get_file",
        "get_commits",
        "get_branches",
        "get_pull_requests",
        "get_contributors",
        "get_releases",
        "analyze_repository",
        
    }

    assert tool_names == expected_tools





def test_mcp_tool_schemas():
    async def get_tools():
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.server"],
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                await session.initialize()
                result = await session.list_tools()
                return {
                    tool.name: tool.input_schema
                    for tool in result.tools
                }

    schemas = asyncio.run(get_tools())

    assert schemas["get_repository"]["required"] == [
        "owner",
        "repo",
    ]

    assert schemas["get_file"]["required"] == [
        "owner",
        "repo",
        "path",
    ]

    assert schemas["search_repositories"]["required"] == [
        "query",
    ]

    assert schemas["search_code"]["required"] == [
        "query",
    ]


def test_mcp_analyze_repository_description():
    async def get_tool():
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.server"],
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                await session.initialize()
                result = await session.list_tools()

                return next(
                    tool
                    for tool in result.tools
                    if tool.name == "analyze_repository"
                )

    tool = asyncio.run(get_tool())

    assert "reconnaissance" in tool.description.lower()
    assert "files" in tool.description.lower()
    assert "technologies" in tool.description.lower()
    assert "domains" in tool.description.lower()
    assert "apis" in tool.description.lower()
    assert "security findings" in tool.description.lower()


def test_mcp_analyze_repository(monkeypatch):
    class FakeResult:
        files = [
            FileIndicator(
                name="README.md",
                path="README.md",
                extension=".md",
                category="documentation",
            )
        ]

        technologies = [
            TechnologyIndicator(
                name="Python",
                category="language",
                evidence=["requirements.txt"],
            )
        ]

        domains = [
            DomainIndicator(
                domain="example.com",
                evidence=["README.md"],
            )
        ]

        apis = [
            ApiIndicator(
                url="/api/users",
                method="GET",
                evidence=["app.py"],
            )
        ]

        security_findings = [
            SecurityFinding(
                indicator_type="test_secret",
                file_path="config.py",
                evidence="redacted-test-evidence",
                severity="low",
                confidence=0.8,
                requires_review=True,
            )
        ]

    class FakeService:
        def __init__(self, repository_recon_service):
            self.repository_recon_service = repository_recon_service

        def analyze_repository(self, owner, repo):
            assert owner == "microsoft"
            assert repo == "vscode"
            return FakeResult()

    import app.mcp.server as server_module

    monkeypatch.setattr(
        server_module,
        "ReconAnalysisService",
        FakeService,
    )

    result = server_module.analyze_repository(
        owner="microsoft",
        repo="vscode",
    )

    assert result == {
        "files": [
            {
                "name": "README.md",
                "path": "README.md",
                "extension": ".md",
                "category": "documentation",
            }
        ],
        "technologies": [
            {
                "name": "Python",
                "category": "language",
                "evidence": ["requirements.txt"],
            }
        ],
        "domains": [
            {
                "domain": "example.com",
                "evidence": ["README.md"],
            }
        ],
        "apis": [
            {
                "url": "/api/users",
                "method": "GET",
                "evidence": ["app.py"],
            }
        ],
        "security_findings": [
            {
                "indicator_type": "test_secret",
                "file_path": "config.py",
                "evidence": "redacted-test-evidence",
                "severity": "low",
                "confidence": 0.8,
                "requires_review": True,
            }
        ],
    }

def test_mcp_get_repository_contents():
    async def call_tool():
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.server"],
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                await session.initialize()

                return await session.call_tool(
                    "get_repository_contents",
                    {
                        "owner": "microsoft",
                        "repo": "vscode",
                        "path": "",
                    },
                )

    result = asyncio.run(call_tool())

    assert result.is_error is False
    assert result.content


@pytest.mark.integration
def test_mcp_search_repositories():
    async def call_tool():
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.server"],
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                await session.initialize()

                return await session.call_tool(
                    "search_repositories",
                    {
                        "query": "language:python",
                        "page": 1,
                        "per_page": 5,
                    },
                )

    result = asyncio.run(call_tool())

    assert result.is_error is False
    assert result.content



if __name__ == "__main__":
    asyncio.run(run_mcp_test())


