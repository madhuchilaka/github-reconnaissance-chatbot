from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(
        self,
        server_command: str = "python",
        server_args: list[str] | None = None,
    ) -> None:
        self.server_params = StdioServerParameters(
            command=server_command,
            args=server_args or ["-m", "app.mcp.server"],
        )

    async def list_tools(self):
        async with stdio_client(self.server_params) as (
            read_stream,
            write_stream,
        ):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                await session.initialize()
                result = await session.list_tools()
                return result

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):
        async with stdio_client(self.server_params) as (
            read_stream,
            write_stream,
        ):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                await session.initialize()

                return await session.call_tool(
                    tool_name,
                    arguments,
                )