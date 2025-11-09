from pathlib import Path


def _load_system_prompt():
    """
    加载系统提示词
    """
    try:
        prompt_path = Path(__file__).resolve().parent.parent.parent / "resources" / "SystemPrompt.txt"
        return prompt_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"警告: 无法加载系统提示词: {e}")
        return "默认系统提示词"


SYSTEM_PROMPT: str = _load_system_prompt()
"""
系统提示词
"""

TOPIC_LIST = [
    "艺术",
    "音乐",
    "影视与动漫",
    "游戏",
    "情感",
    "两性与关系",
    "育儿与家庭",
    "宠物",
    "职场技能",
    "教育",
    "科技",
    "超自然现象",
    "体育",
    "医疗",
    "政治",
    "法律",
    "社会",
    "经济",
    "商业与金融",
    "时尚与潮流",
    "军事",
    "农业",
    "历史",
    "哲学",
    "宗教",
    "环境",
    "法律",
    "美食",
    "旅游",
    "家居",
]
