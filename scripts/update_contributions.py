"""Rebuilds the open source contributions table in the README from GitHub search.

Finds the user's public PRs outside their own repositories and skips ones that
were closed without being merged. Custom descriptions come from
contributions.json; a PR without one is listed with its own title.
"""

import json
import os
import pathlib
import re
import urllib.parse
import urllib.request

USER = os.environ.get("GITHUB_USER", "moosyroot")
ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
DESCRIPTIONS = ROOT / "contributions.json"
START, END = "<!-- CONTRIBUTIONS:START -->", "<!-- CONTRIBUTIONS:END -->"

STATUS = {"merged": "✅ Merged", "open": "🟡 In review"}


def search_prs():
    query = f"is:pr author:{USER} -user:{USER} is:public"
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": query, "sort": "created", "order": "desc", "per_page": 100}
    )
    headers = {"Accept": "application/vnd.github+json"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
        return json.load(response)["items"]


def build_table(items, descriptions):
    rows = []
    for item in items:
        if item["pull_request"].get("merged_at"):
            status = "merged"
        elif item["state"] == "open":
            status = "open"
        else:
            continue
        repo = item["repository_url"].removeprefix("https://api.github.com/repos/")
        text = descriptions.get(item["html_url"], item["title"]).replace("|", "\\|")
        rows.append(
            f"| [{repo}](https://github.com/{repo}) | [{text}]({item['html_url']}) | {STATUS[status]} |"
        )
    if not rows:
        return "_No open source contributions yet._"
    return "\n".join(["| Project | Contribution | Status |", "| --- | --- | --- |", *rows])


def main():
    descriptions = json.loads(DESCRIPTIONS.read_text()) if DESCRIPTIONS.exists() else {}
    table = build_table(search_prs(), descriptions)
    readme = README.read_text()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        raise SystemExit(f"Could not find the {START} ... {END} markers in README")
    README.write_text(pattern.sub(lambda _: f"{START}\n{table}\n{END}", readme))


if __name__ == "__main__":
    main()
