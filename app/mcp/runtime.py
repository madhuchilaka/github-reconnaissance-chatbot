import asyncio

from app.mcp.client import MCPClient


class MCPRuntime:
    def __init__(self, client: MCPClient):
        self.client = client

    def list_tools(self):
        return asyncio.run(self.client.list_tools())

    def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):
        return asyncio.run(
            self.client.call_tool(
                tool_name,
                arguments,
            )
        )