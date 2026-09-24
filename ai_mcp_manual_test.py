from app.ai.agent import AIAgent
from app.ai.client import AIClient
from app.mcp.client import MCPClient
from app.mcp.runtime import MCPRuntime


class FakeToolCall:
    type = "function_call"
    name = "get_repository"
    arguments = '{"owner": "microsoft", "repo": "vscode"}'
    call_id = "smoke_call_1"


class FakeFirstResponse:
    output = [FakeToolCall()]


class FakeFinalResponse:
    output = []
    output_text = "Repository information successfully retrieved through MCP."


class FakeResponses:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)

        if len(self.calls) == 1:
            return FakeFirstResponse()

        return FakeFinalResponse()


runtime = MCPRuntime(MCPClient())

ai_client = AIClient()

fake_responses = FakeResponses()
ai_client.client.responses = fake_responses

agent = AIAgent(
    ai_client,
    runtime,
)

result = agent.respond(
    "Get information about microsoft/vscode"
)

print("AI result:", result)
print("Model calls:", len(fake_responses.calls))
print("Tools supplied to model:", len(agent.tools))