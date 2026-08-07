"""
Hacker News Collector. 职责边界：只读取/保存/记录，不判断是否是机会。
"""
import requests

BASE = "https://hacker-news.firebaseio.com/v0"


def collect(max_items):
    ids = requests.get(f"{BASE}/newstories.json", timeout=15).json()[:max_items]
    signals = []
    for item_id in ids:
        item = requests.get(f"{BASE}/item/{item_id}.json", timeout=15).json()
        if not item or item.get("type") != "story":
            continue
        signals.append({
            "source": "hackernews",
            "external_id": str(item.get("id")),
            "title": item.get("title", ""),
            "url": item.get("url") or f"https://news.ycombinator.com/item?id={item.get('id')}",
            "text": item.get("text", "") or "",
            "created_at": item.get("time"),
            "score": item.get("score", 0),
            "raw": item,
        })
    return signals
