# Opportunity Discovery — Level 1 最小闭环

对应记忆文件 `opportunity_discovery_loop.md` 的"第一版最小闭环"：HN + GitHub + Stack Exchange 三个 Source。

## 运行

```bash
pip install -r requirements.txt
python run.py
```

## 处理链

```
Collectors (hackernews/github/stackexchange)
  -> Normalize/Dedupe (pipeline/normalize.py)
  -> Classify (pipeline/classify.py，8类信号，关键词启发式)
  -> Cluster (pipeline/cluster.py，单条信号不生成机会)
  -> Score (pipeline/score.py，六项打分 0-12)
  -> Candidate Opportunity Pool (data/candidate_pool.json)
```

## 边界（严格对应架构文档，不要越权）

- 本系统止步于 Candidate Opportunity Pool。**不做 Human Review**——`human_review_status` 字段留空(`PENDING`)，由人工在 `data/candidate_pool.json` 里手动改成 `APPROVE`/`WATCH`/`REJECT`。
- 不做 Level 0（行业分析）、Level 2（4D-5L-6G）、Level 2.5（Validation）——那些是独立系统。
- Classification 与 Actor/Need/Current Solution/Friction 抽取目前是关键词启发式 MVP，不是ML/LLM判断，得分和分类仅供参考，不是最终结论。
- Feedback Loop（456结果回流更新关键词库/Source权重/筛选权重/个人约束过滤规则）**尚未实现**，是已知的下一步。

## Data Validation（2026-08-07，不改架构，不加语义相似度）

按用户决定：现在不升级 Semantic Matching，先证明"跨来源重复=机会信号"这个假设本身值不值得投入优化。

流程：
1. 连续跑 `python run.py` 若干轮（**跨天跑才有意义**——HN newstories/GitHub 14天新建仓库/SE 最新活跃问题，短时间内重复运行数据几乎不变，同一天内多次运行不会带来新增样本）
2. 攒够几轮 `data/raw/*.json` 后，跑 `python sample_for_review.py 40` 抽样导出到 `data/review_sample.csv`
3. 人工打开 CSV，把认为属于同一机会的行填相同 `cluster_id`
4. 检查三件事：是否存在跨来源重复表达同一机会的样本 / 人类能否稳定判断 / 占比高不高
5. 只有当①②③都成立，才有理由升级语义相似度；如果人工也找不出明显 cluster，说明"重复出现"本身可能不是这个市场里的主要机会发现机制，需要重审 Level 1 假设而不是升级算法

`sample_for_review.py` 抽样时只按 `source+external_id` 去重，**不做标题相似度判断**——特意跳过 `pipeline/normalize.py` 那层，避免用待验证的假设本身去筛选验证它的样本。

## 已验证的真实限制（不是猜测，是实测结果）

跑了一次 300 条信号（HN/GitHub/SE 各100），**0 个 Cluster**。原因：`normalize.dedupe()` 的跨来源重复判定是标题级词面重叠（阈值0.6），但同一个话题在 HN 标题、GitHub 仓库名、SE 问题标题里几乎不会用相同的词——比如同一个"AI笔记工具"需求，HN 可能叫"Show HN: my note app"，GitHub 仓库叫"quicknote"，两者重叠度是0。**结论：目前 Level 1 只做到了"收集"，"发现"（跨信号识别同一机会）基本没有真正生效**，需要后续升级为语义相似度（embedding）或人工关键词库匹配，而不是词面重叠。这条不是理论上的风险提示，是这次实测直接暴露的。

## 已知限制

- HN collector 按 id 逐条请求 detail，量大时较慢。
- 打分/分类关键词是启发式初版，需要跑几轮真实数据后人工校准。
- 无鉴权/去重持久化跨运行状态之外的机制，重复运行会不断往候选池追加（按 url 在 normalize 阶段做了单次运行内去重，但跨运行去重未做，后续需要在 candidate_pool 层加 url 唯一性检查）。
