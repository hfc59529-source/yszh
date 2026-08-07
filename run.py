"""
Level 1 最小闭环入口：
Source Collectors -> Normalize/Dedupe -> Classify -> Cluster -> Score -> Candidate Opportunity Pool

只写候选池数据，不做 Human Review（人工审核这一步在系统外，由人读 candidate_pool.json 完成）。
"""
import sys
from datetime import datetime, timezone

import config
from collectors import hackernews, github, stackexchange
from pipeline.normalize import dedupe
from pipeline.classify import classify_all
from pipeline.cluster import build_clusters
from pipeline.score import score_all
from storage import load_json, save_json


def collect_all():
    signals = []
    try:
        signals += hackernews.collect(config.HN_MAX_ITEMS)
    except Exception as e:
        print(f"[warn] hackernews collector failed: {e}", file=sys.stderr)
    try:
        signals += github.collect(config.GITHUB_MAX_REPOS)
    except Exception as e:
        print(f"[warn] github collector failed: {e}", file=sys.stderr)
    try:
        signals += stackexchange.collect(config.STACKEXCHANGE_MAX_QUESTIONS, config.STACKEXCHANGE_SITE)
    except Exception as e:
        print(f"[warn] stackexchange collector failed: {e}", file=sys.stderr)
    return signals


def main():
    run_at = datetime.now(timezone.utc).isoformat()

    raw_signals = collect_all()
    print(f"collected {len(raw_signals)} raw signals")
    save_json(f"{config.RAW_DIR}/{run_at}.json", raw_signals)

    deduped = dedupe(raw_signals)
    print(f"{len(deduped)} signals after dedupe")

    classified = classify_all(deduped)
    clusters = build_clusters(classified)
    print(f"{len(clusters)} clusters formed (single-signal items dropped, not opportunities)")

    scored = score_all(clusters)

    pool = load_json(config.CANDIDATE_POOL_PATH, [])
    for c in scored:
        if c["score"]["status"] == "ARCHIVE":
            continue  # 0-4分不进候选池
        pool.append({
            "run_at": run_at,
            "title": c["primary_signal"]["title"],
            "url": c["primary_signal"]["url"],
            "sources": c["sources"],
            "cluster_size": c["cluster_size"],
            "classification": c["primary_signal"]["classification"],
            "score": c["score"],
            "human_review_status": "PENDING",  # APPROVE / WATCH / REJECT，由人工填写
        })

    save_json(config.CANDIDATE_POOL_PATH, pool)
    print(f"candidate pool now has {len(pool)} entries -> {config.CANDIDATE_POOL_PATH}")


if __name__ == "__main__":
    main()
