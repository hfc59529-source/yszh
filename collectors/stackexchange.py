"""
Stack Exchange Collector. 职责边界：只读取/保存/记录，不判断是否是机会。
高频具体问题 = 未解决需求信号。
"""
import requests

API = "https://api.stackexchange.com/2.3/questions"


def collect(max_items, site="stackoverflow"):
    params = {
        "order": "desc",
        "sort": "activity",
        "site": site,
        "pagesize": min(max_items, 100),
        "filter": "!9_bDDxJY5",  # includes body
    }
    resp = requests.get(API, params=params, timeout=15)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    signals = []
    for q in items:
        signals.append({
            "source": "stackexchange",
            "external_id": str(q.get("question_id")),
            "title": q.get("title", ""),
            "url": q.get("link", ""),
            "text": q.get("body", "") or "",
            "created_at": q.get("creation_date"),
            "score": q.get("score", 0),
            "raw": {k: q.get(k) for k in ("tags", "view_count", "answer_count", "is_answered")},
        })
    return signals
