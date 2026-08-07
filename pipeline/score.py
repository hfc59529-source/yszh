"""
六项打分（每项0-2分）：Repetition / Pain / Spend / Supply Gap / Reachability / Testability。
决定能否进入候选池，不决定项目是否成立。
"""
from config import SCORING_KEYWORDS, SCORE_THRESHOLDS


def _keyword_score(text, keywords):
    hits = sum(1 for kw in keywords if kw in text)
    if hits == 0:
        return 0
    if hits == 1:
        return 1
    return 2


def score_cluster(cluster):
    primary = cluster["primary_signal"]
    text = f"{primary.get('title', '')} {primary.get('text', '')}".lower()

    repetition = min(cluster["cluster_size"] - 1, 2)  # 2+支持信号封顶2分
    pain = _keyword_score(text, SCORING_KEYWORDS["pain"])
    spend = _keyword_score(text, SCORING_KEYWORDS["spend"])
    supply_gap = _keyword_score(text, SCORING_KEYWORDS["supply_gap"])
    reachability = 2 if primary.get("url") else 0
    testability = _keyword_score(text, SCORING_KEYWORDS["testability"])

    total = repetition + pain + spend + supply_gap + reachability + testability

    status = "ARCHIVE"
    for label, (lo, hi) in SCORE_THRESHOLDS.items():
        if lo <= total <= hi:
            status = label
            break

    return {
        "repetition": repetition,
        "pain": pain,
        "spend": spend,
        "supply_gap": supply_gap,
        "reachability": reachability,
        "testability": testability,
        "total": total,
        "status": status,
    }


def score_all(clusters):
    scored = []
    for c in clusters:
        c["score"] = score_cluster(c)
        scored.append(c)
    return scored
