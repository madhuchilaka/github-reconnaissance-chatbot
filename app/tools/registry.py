from app.tools.definitions import (
    GET_BRANCHES_TOOL,
    GET_COMMITS_TOOL,
    GET_CONTRIBUTORS_TOOL,
    GET_FILE_TOOL,
    GET_PULL_REQUESTS_TOOL,
    GET_RELEASES_TOOL,
    GET_REPOSITORY_CONTENTS_TOOL,
    GET_REPOSITORY_TOOL,
    SEARCH_CODE_TOOL,
    SEARCH_REPOSITORIES_TOOL,
)
class ToolRegistry:
    def __init__(self):
        self._tools = {
            SEARCH_REPOSITORIES_TOOL["name"]: SEARCH_REPOSITORIES_TOOL,
            GET_REPOSITORY_TOOL["name"]: GET_REPOSITORY_TOOL,
            GET_REPOSITORY_CONTENTS_TOOL["name"]: GET_REPOSITORY_CONTENTS_TOOL,
            SEARCH_CODE_TOOL["name"]: SEARCH_CODE_TOOL,
            GET_FILE_TOOL["name"]: GET_FILE_TOOL,
            GET_COMMITS_TOOL["name"]: GET_COMMITS_TOOL,
            GET_BRANCHES_TOOL["name"]: GET_BRANCHES_TOOL,
            GET_PULL_REQUESTS_TOOL["name"]: GET_PULL_REQUESTS_TOOL,
            GET_CONTRIBUTORS_TOOL["name"]: GET_CONTRIBUTORS_TOOL,
            GET_RELEASES_TOOL["name"]: GET_RELEASES_TOOL,
        }

    def get(self, name: str) -> dict:
        return self._tools[name]

    def all(self) -> list[dict]:
        return list(self._tools.values())