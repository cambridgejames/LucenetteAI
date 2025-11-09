from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict


FUNCTION_LIST: List[dict] = []
FUNCTION_MAP: Dict[str, "LlmFunctionTool"] = {}


@dataclass
class FunctionInfo(object):
    name: str
    description: str
    parameters: dict

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class LlmFunctionTool(ABC):
    """
    语言模型工具抽象类
    """
    def __init__(self):
        function_info: FunctionInfo = self.get_tool_info()
        FUNCTION_MAP.update({
            function_info.name: self,
        })
        FUNCTION_LIST.append({
            "type": "function",
            "function": function_info.to_dict(),
        })

    @abstractmethod
    def get_tool_info(self) -> FunctionInfo:
        """
        获取语言模型工具信息
        :return: 返回一个字典，包含语言模型工具的相关信息
        """
        pass

    @abstractmethod
    def execute(self, params: dict) -> str:
        """
        执行语言模型工具逻辑
        :return: 返回执行结果的字符串
        """
        pass
