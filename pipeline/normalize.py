"""
Normalize / Clean / Deduplicate. 三层去重：完全重复 / 近似重复 / 跨来源重复。
不判断是否是机会，只清洗和归并支持信号。
"""
import re


def _norm_title(title):
    title = title.lower()
    title = re.sub(r"[^a-z0-9一-鿿\s]", "", title)
    return set(title.split())


def dedupe(signals):
    seen_urls = set()
    deduped = []
    title_sets = []

    for s in signals:
        # 完全重复：同一 url
        if s["url"] and s["url"] in seen_urls:
            continue

        tokens = _norm_title(s["title"])
        is_near_dup = False
        for existing_idx, existing_tokens in enumerate(title_sets):
            if not tokens or not existing_tokens:
                continue
            overlap = len(tokens & existing_tokens) / max(len(tokens | existing_tokens), 1)
            # 跨来源重复：标题高度相似，合并为同一机会的多条支持信号
            if overlap >= 0.6:
                deduped[existing_idx].setdefault("supporting_signals", []).append(s)
                is_near_dup = True
                break

        if is_near_dup:
            continue

        seen_urls.add(s["url"])
        title_sets.append(tokens)
        s["supporting_signals"] = []
        deduped.append(s)

    return deduped
