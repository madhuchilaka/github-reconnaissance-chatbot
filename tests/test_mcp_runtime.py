from app.mcp.client import MCPClient
from app.mcp.runtime import MCPRuntime
from app.ai.tools import get_openai_tools_from_mcp
import pytest

def test_mcp_runtime_lists_tools():
    runtime = MCPRuntime(MCPClient())

    result = runtime.list_tools()

    tool_names = {tool.name for tool in result.tools}

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

@pytest.mark.integration
def test_mcp_runtime_calls_tool():
    runtime = MCPRuntime(MCPClient())

    result = runtime.call_tool(
        "get_repository",
        {
            "owner": "microsoft",
            "repo": "vscode",
        },
    )

    assert result.is_error is False
    assert result.content


def test_mcp_tools_convert_to_openai_tools():
    runtime = MCPRuntime(MCPClient())

    tools = get_openai_tools_from_mcp(runtime)

    assert len(tools) == 11
    assert tools[0]["type"] == "function"
    assert tools[0]["name"] == "get_repository"
    assert "description" in tools[0]
    assert "parameters" in tools[0]