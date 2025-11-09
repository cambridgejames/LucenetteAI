from typing import Generator, Any, List

import requests

from python.cbb import JsonUtil
from python.chat.ChatModels import TypedResponseMessage, MessageType, OllamaRequestBody, TypedContextMessage, RoleType
from python.config.constant import OLLAMA_API_BASE_URL, OLLAMA_API_CHAT
from python.config.prompts import SYSTEM_PROMPT
from python.tools.abc.LlmFunctionManager import LlmFunctionManager


OLLAMA_API_CHAT_FULL: str = OLLAMA_API_BASE_URL + OLLAMA_API_CHAT


class ChatContext:
    """
    LLM对话上下文
    """

    __context_index: int
    __context_length: int
    __model_name: str
    __message_context: List[TypedContextMessage]
    __message_length: int

    def __init__(self, index: int, context_length: int, model_name: str):
        """
        构造函数
        :param index: 上下文编码
        :param model_name: 模型名称
        """
        self.__context_index: int = index
        self.__context_length: int = context_length
        self.__model_name: str = model_name
        self.__message_context: List[TypedContextMessage] = [
            TypedContextMessage(RoleType.SYSTEM, SYSTEM_PROMPT, None),
        ]
        self.__message_length: int = 0

    def get_index(self) -> int:
        return self.__context_index

    def get_model_name(self) -> str:
        return self.__model_name

    def append_message(self, role: RoleType, message: Any) -> None:
        """
        添加消息至上下文
        :param role: 消息来源
        :param message: 消息体
        """
        real_message: str = JsonUtil.to_json(message)
        self.__message_context.append(TypedContextMessage(role, real_message, None))
        self.__message_length = self.__message_length + len(real_message)
        self.__message_normalize()

    def append_tool_message(self, index: int, message: str) -> None:
        """
        添加工具返回结果至上下文
        :param index: 方法调用编码
        :param message: 方法返回体
        """
        self.__message_context.append(TypedContextMessage(RoleType.TOOL, message, index))
        self.__message_length = self.__message_length + len(message)
        self.__message_normalize()

    def __message_normalize(self) -> None:
        """
        标准化消息上下文（删除超出长度的历史消息）
        """
        if self.__message_length <= self.__context_length:
            return
        temp_messages: List[TypedContextMessage | None] = self.__message_context.copy()
        current_length = self.__message_length
        message_index: int = 0
        while message_index < len(temp_messages) and current_length > self.__context_length:
            current_message: TypedContextMessage = temp_messages[message_index]
            if current_message.role == RoleType.SYSTEM:
                message_index += 1
                continue
            temp_messages[message_index] = None
            current_length -= len(current_message.content)

            # 继续删除后面连续的tool消息
            message_index += 1
            while message_index < len(temp_messages) and temp_messages[message_index].role == RoleType.TOOL:
                current_length -= len(temp_messages[message_index].content)
                temp_messages[message_index] = None
                message_index += 1

        self.__message_context = [item for item in temp_messages if item is not None]
        self.__message_length = current_length

    def stream_response(self) -> Generator[TypedResponseMessage, Any, None]:
        """
        向Ollama模型发送单个对话请求，解析对话结果并通过流式返回
        :return: 对话结果迭代器
        """
        data: OllamaRequestBody = OllamaRequestBody(
            model=self.__model_name,
            messages=self.__message_context,
            tools=LlmFunctionManager.get_tool_infos(),
            stream=True,
        )
        try:
            with requests.post(OLLAMA_API_CHAT_FULL, data=JsonUtil.to_json(data), stream=True) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=None):
                    chunk_data: dict = JsonUtil.from_json(chunk.decode("utf-8"))
                    if chunk_data.get("done", True):
                        break
                    if not "message" in chunk_data:
                        continue
                    current_message: dict = chunk_data.get("message", {})
                    message_yield: bool = False
                    for solvable_type in sorted(MessageType, key=lambda x: x.get_index()):
                        type_key: str = solvable_type.get_key()
                        if type_key in current_message and current_message[type_key]:
                            yield TypedResponseMessage(solvable_type, current_message[type_key])
                            message_yield = True
                            break
                    if not message_yield:
                        raise SystemError(f"Unsupported message type for: {current_message}")
        except requests.exceptions.RequestException as e:
            raise SystemError(f"Request failed: {e}")
