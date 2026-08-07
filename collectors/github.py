"""
GitHub Collector. 职责边界：只读取/保存/记录，不判断是否是机会。
用 Search API 找最近创建、star增长快的仓库，作为"新供给"信号。
"""
import requests
from datetime import datetime, timedelta

API = "https://api.github.com/search/repositories"


def collect(max_items):
    since = (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%d")
    params = {
        "q": f"created:>{since}",
        "sort": "stars",
        "order": "desc",
        "per_page": min(max_items, 100),
    }
    resp = requests.get(API, params=params, timeout=15, headers={"Accept": "application/vnd.github+json"})
    resp.raise_for_status()
    items = resp.json().get("items", [])
    signals = []
    for repo in items:
        signals.append({
            "source": "github",
            "external_id": str(repo.get("id")),
            "title": repo.get("full_name", ""),
            "url": repo.get("html_url", ""),
            "text": repo.get("description", "") or "",
            "created_at": repo.get("created_at"),
            "score": repo.get("stargazers_count", 0),
            "raw": {k: repo.get(k) for k in ("full_name", "description", "language", "topics")},
        })
    return signals
