"""
Level 1 最小闭环配置：三个Source（Hacker News / GitHub / Stack Exchange）。
对应记忆文件 opportunity_discovery_loop.md 中的"第一版最小闭环"。
"""

DATA_DIR = "data"
RAW_DIR = f"{DATA_DIR}/raw"
CANDIDATE_POOL_PATH = f"{DATA_DIR}/candidate_pool.json"
SIGNALS_PATH = f"{DATA_DIR}/signals.json"

# 抓取窗口：每次运行取最近多少条/多少页，避免第一版全量爬取
HN_MAX_ITEMS = 100
GITHUB_MAX_REPOS = 100
STACKEXCHANGE_MAX_QUESTIONS = 100

STACKEXCHANGE_SITE = "stackoverflow"

# 8类信号关键词启发式（MVP：关键词匹配，非ML/LLM分类，后续可替换）
CLASSIFICATION_KEYWORDS = {
    "QUESTION": ["how to", "how do i", "is there a way", "what's the best way", "怎么", "如何"],
    "COMPLAINT": ["hate", "annoying", "frustrated", "sucks", "broken", "why does", "terrible"],
    "REQUEST": ["please add", "feature request", "wish there was", "would be nice", "looking for"],
    "PURCHASE": ["bought", "paid for", "subscription", "pricing", "worth it", "$"],
    "REVIEW": ["review", "compared", "vs", "alternative to", "better than"],
    "NEW_SUPPLY": ["show hn", "launched", "introducing", "released", "we built", "we made"],
    "TREND": ["trend", "rising", "growing", "everyone is", "the future of"],
    "FAILURE": ["shut down", "failed", "discontinued", "deprecated", "abandoned"],
}

# 六项打分关键词（0-2分，启发式，非权威结论）
SCORING_KEYWORDS = {
    "pain": ["hate", "annoying", "frustrated", "broken", "terrible", "sucks"],
    "spend": ["paid", "pricing", "subscription", "$", "budget", "cost"],
    "supply_gap": ["no alternative", "nothing like", "doesn't exist", "wish there was", "looking for"],
    "testability": ["mvp", "prototype", "beta", "waitlist"],
}

SCORE_THRESHOLDS = {
    "ARCHIVE": (0, 4),
    "WATCH": (5, 7),
    "CANDIDATE": (8, 9),
    "PRIORITY": (10, 12),
}
