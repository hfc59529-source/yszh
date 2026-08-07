"""
Clustering：只有 Cluster 才能进入机会识别，单条信号不允许直接生成机会。
normalize.dedupe() 已经把近似重复/跨来源重复的信号合并进 supporting_signals，
这里只做门槛判断：cluster size(自身+支持信号) >= 2 才算一个 Cluster，进入 Opportunity Detection。
"""


def build_clusters(deduped_signals):
    clusters = []
    for s in deduped_signals:
        supporting = s.get("supporting_signals", [])
        size = 1 + len(supporting)
        if size < 2:
            continue  # 单条信号，不生成机会，留在原始信号池，不进候选池
        clusters.append({
            "primary_signal": s,
            "supporting_signals": supporting,
            "cluster_size": size,
            "sources": sorted({s["source"], *[x["source"] for x in supporting]}),
        })
    return clusters
