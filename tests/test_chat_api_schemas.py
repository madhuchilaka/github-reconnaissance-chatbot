from app.api.schemas import ChatRequest, ChatResponse


def test_chat_request_accepts_message():
    request = ChatRequest(
        message="Analyze microsoft/vscode",
    )

    assert request.message == "Analyze microsoft/vscode"


def test_chat_response_accepts_response():
    response = ChatResponse(
        response="Repository analysis completed.",
    )

    assert response.response == "Repository analysis completed."