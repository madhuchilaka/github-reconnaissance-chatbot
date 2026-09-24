from app.tools.errors import ToolExecutionError
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.results import ToolResult
from app.tools.validation import (
    validate_get_branches_arguments,
    validate_get_commits_arguments,
    validate_get_contributors_arguments,
    validate_get_file_arguments,
    validate_get_pull_requests_arguments,
    validate_get_repository_arguments,
    validate_get_repository_contents_arguments,
    validate_search_code_arguments,
    validate_search_repositories_arguments,
    validate_get_releases_arguments
)

class ToolDispatcher:
    def __init__(
        self,
        executor: ToolExecutor,
        registry: ToolRegistry,
    ):
        self.executor = executor
        self.registry = registry

    def dispatch(self, tool_name: str, arguments: dict) -> ToolResult:
        try:
            self.registry.get(tool_name)
        except KeyError:
            raise ValueError(f"Unknown tool: {tool_name}")

        if tool_name == "search_repositories":
            validate_search_repositories_arguments(arguments)

            try:
                data = self.executor.search_repositories(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )


        if tool_name == "search_code":
            validate_search_code_arguments(arguments)

            try:
                data = self.executor.search_code(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )
        

        if tool_name == "get_repository":
            validate_get_repository_arguments(arguments)

            try:
                data = self.executor.get_repository(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )

        if tool_name == "get_repository_contents":
            validate_get_repository_contents_arguments(arguments)

            try:
                data = self.executor.get_repository_contents(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )


        if tool_name == "get_file":
            validate_get_file_arguments(arguments)

            try:
                data = self.executor.get_file(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )


        if tool_name == "get_commits":
            validate_get_commits_arguments(arguments)

            try:
                data = self.executor.get_commits(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )


        if tool_name == "get_branches":
            validate_get_branches_arguments(arguments)

            try:
                data = self.executor.get_branches(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )


        if tool_name == "get_pull_requests":
            validate_get_pull_requests_arguments(arguments)

            try:
                data = self.executor.get_pull_requests(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )


        if tool_name == "get_contributors":
            validate_get_contributors_arguments(arguments)

            try:
                data = self.executor.get_contributors(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )


        if tool_name == "get_releases":
            validate_get_releases_arguments(arguments)

            try:
                data = self.executor.get_releases(**arguments)
            except ToolExecutionError as exc:
                return ToolResult.error_result(
                    tool_name,
                    str(exc),
                )

            return ToolResult.success_result(
                tool_name,
                data,
            )


        raise ValueError(f"Tool is registered but not implemented: {tool_name}")






    