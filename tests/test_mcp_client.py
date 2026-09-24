import asyncio

from app.mcp.client import MCPClient


def test_mcp_client_discovers_all_tools():
    async def discover_tools():
        client = MCPClient()
        result = await client.list_tools()
        return {tool.name for tool in result.tools}

    tool_names = asyncio.run(discover_tools())

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

def test_mcp_client_calls_get_repository():
    async def call_tool():
        client = MCPClient()

        return await client.call_tool(
            "get_repository",
            {
                "owner": "microsoft",
                "repo": "vscode",
            },
        )

    result = asyncio.run(call_tool())

    assert result.is_error is False
    assert result.content