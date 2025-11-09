from typing import List

from python.tools.abc.LlmFunctionTool import FUNCTION_LIST, FUNCTION_MAP
from python.tools.impl.ssearch.DuckduckgoWebSearch import DuckduckgoWebSearch
from python.tools.impl.topic.TopicList import TopicList


def _init_function_instance_list() -> None:
    # BaiduWebSearch()
    DuckduckgoWebSearch()
    TopicList()


class LlmFunctionManager(object):
    """
    工具调用管理器
    """

    @classmethod
    def get_tool_infos(cls) -> List[dict]:
        """
        获取全部的工具描述列表
        :return: 工具描述列表
        """
        if len(FUNCTION_LIST) == 0:
            _init_function_instance_list()
        return FUNCTION_LIST

    @classmethod
    def execute(cls, function_name: str, params: dict) -> str:
        """
        调用工具方法
        :param function_name: 工具名称
        :param params: 参数列表
        :return: 调用结果
        """
        if not function_name in FUNCTION_MAP:
            return "请求失败"
        try:
            return FUNCTION_MAP[function_name].execute(params)
        except Exception:
            return "请求失败"
