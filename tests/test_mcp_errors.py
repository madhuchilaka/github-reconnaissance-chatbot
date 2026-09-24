import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_invalid_repository_test():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_repository",
                {
                    "owner": "",
                    "repo": "vscode",
                },
            )

            return result


def test_invalid_repository_owner_returns_mcp_error():
    result = asyncio.run(run_invalid_repository_test())

    assert result.is_error is True
    assert result.content



