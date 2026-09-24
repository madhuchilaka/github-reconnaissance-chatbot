SEARCH_REPOSITORIES_TOOL = {
    "name": "search_repositories",
    "description": "Search public GitHub repositories.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "GitHub repository search query.",
            },
            "page": {
                "type": "integer",
                "description": "Page number of search results.",
                "default": 1,
            },
            "per_page": {
                "type": "integer",
                "description": "Number of repositories to return per page.",
                "default": 30,
            },
        },
        "required": ["query"],
    },
}


GET_REPOSITORY_TOOL = {
    "name": "get_repository",
    "description": "Get detailed metadata for a public GitHub repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "GitHub repository owner or organization.",
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository name.",
            },
        },
        "required": ["owner", "repo"],
    },
}



GET_REPOSITORY_CONTENTS_TOOL = {
    "name": "get_repository_contents",
    "description": "Get the contents of a file or directory in a public GitHub repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "GitHub repository owner or organization.",
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository name.",
            },
            "path": {
                "type": "string",
                "description": "Repository path. Use an empty string for the repository root.",
                "default": "",
            },
        },
        "required": ["owner", "repo"],
    },
}


SEARCH_CODE_TOOL = {
    "name": "search_code",
    "description": "Search code within public GitHub repositories.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "GitHub code search query.",
            },
            "page": {
                "type": "integer",
                "description": "Page number of search results.",
                "default": 1,
            },
            "per_page": {
                "type": "integer",
                "description": "Number of code results to return per page.",
                "default": 30,
            },
        },
        "required": ["query"],
    },
}



GET_FILE_TOOL = {
    "name": "get_file",
    "description": "Retrieve a file from a public GitHub repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "GitHub repository owner.",
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository name.",
            },
            "path": {
                "type": "string",
                "description": "Path to the file within the repository.",
            },
        },
        "required": ["owner", "repo", "path"],
    },
}


GET_COMMITS_TOOL = {
    "name": "get_commits",
    "description": "Retrieve commits from a public GitHub repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "GitHub repository owner.",
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository name.",
            },
        },
        "required": ["owner", "repo"],
    },
}



GET_BRANCHES_TOOL = {
    "name": "get_branches",
    "description": "Retrieve branches from a public GitHub repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "GitHub repository owner.",
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository name.",
            },
        },
        "required": ["owner", "repo"],
    },
}



GET_PULL_REQUESTS_TOOL = {
    "name": "get_pull_requests",
    "description": "Retrieve pull requests from a public GitHub repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "GitHub repository owner.",
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository name.",
            },
        },
        "required": ["owner", "repo"],
    },
} 



GET_CONTRIBUTORS_TOOL = {
    "name": "get_contributors",
    "description": "Retrieve contributors from a public GitHub repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "GitHub repository owner.",
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository name.",
            },
        },
        "required": ["owner", "repo"],
    },
}


GET_RELEASES_TOOL = {
    "name": "get_releases",
    "description": "Retrieve releases from a public GitHub repository.",
    "parameters": {
        "type": "object",
        "properties": {
            "owner": {
                "type": "string",
                "description": "GitHub repository owner.",
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository name.",
            },
        },
        "required": ["owner", "repo"],
    },
}