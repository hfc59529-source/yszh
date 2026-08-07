"""
Classification：8类信号（QUESTION/COMPLAINT/REQUEST/PURCHASE/REVIEW/NEW_SUPPLY/TREND/FAILURE）。
MVP用关键词启发式，非ML/LLM，后续可替换 classify() 内部实现而不改调用方。
Actor/Need/Current Solution/Friction 四字段第一版留空占位，需要人工或LLM升级补全，不在此臆造。
"""
from config import CLASSIFICATION_KEYWORDS


def classify(signal):
    text = f"{signal.get('title', '')} {signal.get('text', '')}".lower()
    matched = []
    for label, keywords in CLASSIFICATION_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            matched.append(label)

    signal["classification"] = matched or ["UNCLASSIFIED"]
    signal["fields"] = {
        "actor": None,
        "need": None,
        "current_solution": None,
        "friction": None,
    }  # 占位，MVP不做臆造式抽取
    return signal


def classify_all(signals):
    return [classify(s) for s in signals]
