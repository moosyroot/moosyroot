"""README'deki açık kaynak katkıları tablosunu GitHub aramasından yeniden üretir.

Kullanıcının kendi repoları dışındaki herkese açık PR'larını bulur; reddedilip
kapanmış olanları göstermez. Türkçe açıklamalar contributions.json'dan gelir,
açıklaması olmayan PR kendi başlığıyla yazılır.
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
START, END = "<!-- KATKILAR:BASLA -->", "<!-- KATKILAR:BITIR -->"

STATUS = {"merged": "✅ Kabul edildi", "open": "🟡 İnceleniyor"}


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
        return "_Henüz açık kaynak katkısı yok._"
    return "\n".join(["| Proje | Katkı | Durum |", "| --- | --- | --- |", *rows])


def main():
    descriptions = json.loads(DESCRIPTIONS.read_text()) if DESCRIPTIONS.exists() else {}
    table = build_table(search_prs(), descriptions)
    readme = README.read_text()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        raise SystemExit(f"README'de {START} ... {END} işaretleri bulunamadı")
    README.write_text(pattern.sub(lambda _: f"{START}\n{table}\n{END}", readme))


if __name__ == "__main__":
    main()
