import json

from app.ai.client import AIClient
from app.ai.tools import get_openai_tools_from_mcp
from app.mcp.runtime import MCPRuntime
from app.ai.prompts import RECONNAISSANCE_AGENT_INSTRUCTIONS


class AIAgent:
    def __init__(
        self,
        client: AIClient,
        runtime: MCPRuntime,
        max_iterations: int = 10,
    ):
        self.client = client
        self.runtime = runtime
        self.tools = get_openai_tools_from_mcp(runtime)
        self.max_iterations = max_iterations



    @staticmethod
    def _serialize_tool_result(tool_result) -> str:
        if hasattr(tool_result, "content"):
            content = []

            for item in tool_result.content:
                if hasattr(item, "text"):
                    content.append(item.text)

            return "\n".join(content)

        return json.dumps(tool_result)

    

    def respond(self, user_message: str):
        response = self.client.client.responses.create(
            model="gpt-5-mini",
            instructions=RECONNAISSANCE_AGENT_INSTRUCTIONS,
            input=user_message,
            tools=self.tools,
        )

        for _ in range(self.max_iterations):
            tool_outputs = []

            for item in response.output:
                if item.type != "function_call":
                    continue

                try:
                    arguments = json.loads(item.arguments)
                except json.JSONDecodeError:
                    tool_outputs.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": "Invalid tool arguments: the tool-call arguments were not valid JSON.",
                        }
                    )
                    continue

                try:
                    tool_result = self.runtime.call_tool(
                        item.name,
                        arguments,
                    )

                    output = self._serialize_tool_result(tool_result)

                except Exception:
                    output = "Tool execution failed. The requested tool could not be completed."

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": output,
                    }
                )

            if not tool_outputs:
                return response.output_text

            response = self.client.client.responses.create(
                model="gpt-5-mini",
                instructions=RECONNAISSANCE_AGENT_INSTRUCTIONS,
                input=[
                    *response.output,
                    *tool_outputs,
                ],
                tools=self.tools,
            )

        raise RuntimeError(
            f"Maximum tool-calling iterations exceeded: {self.max_iterations}"
        )