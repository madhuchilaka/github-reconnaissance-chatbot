from app.github.client import GitHubClient


client = GitHubClient()

repository = client.get_repository("microsoft", "vscode")

print("Repository:", repository["full_name"])
print("Description:", repository["description"])
print("Stars:", repository["stargazers_count"])


search_results = client._request_json(
    "GET",
    "/search/repositories",
    params={"q": "microsoft"},
)

print("Search total:", search_results["total_count"])
print("First repository:", search_results["items"][0]["full_name"])
print("First repository keys:", search_results["items"][0].keys())
print("First repository owner:", search_results["items"][0]["owner"])


for item in search_results["items"][:3]:
    print(
        "Candidate:",
        item["full_name"],
        "| Owner:",
        item["owner"]["login"],
        "| Fork:",
        item["fork"],
    )