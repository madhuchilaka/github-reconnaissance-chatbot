from app.tools.registry import ToolRegistry


def get_openai_tools() -> list[dict]:
    registry = ToolRegistry()

    return [
        {
            "type": "function",
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["parameters"],
        }
        for tool in registry.all()
    ]

def get_openai_tools_from_mcp(runtime) -> list[dict]:
    result = runtime.list_tools()

    return [
        {
            "type": "function",
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema,
        }
        for tool in result.tools
    ]