"""
Data Validation 工具：不改架构，不加语义相似度。

用途：把 data/raw/ 下多轮真实采集的信号合并去重（仅按 source+external_id 去重，
不做标题相似度判断——这一步就是为了不预设"标题重叠=同一机会"这个待验证的假设），
随机抽样一批，导出成人工可标注的表格，供人工判断：

1. 是否存在"同一机会被不同来源重复表达"的样本
2. 人类能不能稳定判断它们属于同一机会
3. 这类样本占比高不高

标注列 cluster_id 由人工手填：同一机会的信号填相同的任意字符串/编号，不属于任何机会的留空。
"""
import csv
import glob
import json
import random
import sys

RAW_GLOB = "data/raw/*.json"
OUTPUT_PATH = "data/review_sample.csv"


def load_all_signals():
    signals = []
    seen = set()
    for path in glob.glob(RAW_GLOB):
        with open(path, "r", encoding="utf-8") as f:
            batch = json.load(f)
        for s in batch:
            key = (s["source"], s["external_id"])
            if key in seen:
                continue
            seen.add(key)
            signals.append(s)
    return signals


def main():
    sample_size = int(sys.argv[1]) if len(sys.argv) > 1 else 40

    signals = load_all_signals()
    if not signals:
        print("data/raw/ 下没有信号，先跑几轮 python run.py 再来抽样")
        return

    sample_size = min(sample_size, len(signals))
    sample = random.sample(signals, sample_size)
    sample.sort(key=lambda s: s["source"])

    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "source", "title", "url", "text_snippet", "cluster_id(人工填写)"])
        for i, s in enumerate(sample):
            snippet = (s.get("text") or "")[:200].replace("\n", " ")
            writer.writerow([i, s["source"], s["title"], s["url"], snippet, ""])

    print(f"共 {len(signals)} 条去重后信号（仅按source+id去重，未做标题相似度判断）")
    print(f"抽样 {sample_size} 条 -> {OUTPUT_PATH}")
    print("请人工打开该文件，把属于同一机会的行填上相同的 cluster_id，不属于任何机会的留空。")


if __name__ == "__main__":
    main()
