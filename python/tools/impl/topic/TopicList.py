import random

from python.cbb import JsonUtil
from python.config.prompts import TOPIC_LIST
from python.tools.abc.LlmFunctionTool import LlmFunctionTool, FunctionInfo


FUNCTION_NAME: str = "get_topic_list"
FUNCTION_DESCRIPTION: str = """
查询当前可以讨论的话题列表以及当前系统的推荐话题。
"""


class TopicList(LlmFunctionTool):

    def get_tool_info(self) -> FunctionInfo:
        return FunctionInfo(FUNCTION_NAME, FUNCTION_DESCRIPTION, {
            "type": "object",
            "properties": {},
            "required": [],
        })

    def execute(self, params: dict) -> str:
        return f"你当前可以讨论的话题有：{JsonUtil.to_json(TOPIC_LIST)}，系统随机推荐话题：{random.choice(TOPIC_LIST)}"