from datetime import datetime
from logging import Logger
from typing import List, Iterator

from colorama import Fore, Style

from python.cbb import JsonUtil
from python.cbb.Logger import get_file_logger
from python.chat.ChatContext import ChatContext
from python.chat.ChatModels import MessageType, TypedContextMessage, RoleType
from python.config.constant import OLLAMA_MODEL_NAME_QWEN3_8B, OLLAMA_MODEL_NAME_LLAMA3P1_LATEST
from python.tools.abc.LlmFunctionManager import LlmFunctionManager


LOGGER: Logger = get_file_logger(f"ChatLog_{datetime.now().strftime("%Y%m%d%H%M%S%f")}")
MESSAGE_CONTEXT: List[TypedContextMessage] = []
CHAT_CONTEXT_LIST: List[ChatContext] = [
    ChatContext(0, 40000, OLLAMA_MODEL_NAME_QWEN3_8B),
    ChatContext(1, 40000, OLLAMA_MODEL_NAME_QWEN3_8B),
    ChatContext(2, 128000, OLLAMA_MODEL_NAME_LLAMA3P1_LATEST),
]


def get_chat_context(round_number: int = 0) -> Iterator[ChatContext]:
    """
    遍历LLM上下文实例列表
    :param round_number: 遍历次数
    :return: LLM上下文
    """
    if len(CHAT_CONTEXT_LIST) == 0:
        return
    if round_number <= 0:
        while True:
            for current_context in CHAT_CONTEXT_LIST:
                yield current_context
    else:
        for current_index in range(round_number):
            real_index: int = current_index % len(CHAT_CONTEXT_LIST)
            yield CHAT_CONTEXT_LIST[real_index] # type: ignore


def insert_message(current_chat: int | None, role: RoleType, content: str, index: int | None = None) -> None:
    if content is None or len(content) <= 0:
        return
    if role == RoleType.ASSISTANT:
        for chat_context in CHAT_CONTEXT_LIST:
            if current_chat == chat_context.get_index():
                chat_context.append_message(RoleType.ASSISTANT, content)
            else:
                chat_context.append_message(RoleType.USER, content)
    elif role == RoleType.USER or current_chat is None:
        for chat_context in CHAT_CONTEXT_LIST:
            chat_context.append_message(RoleType.USER, content)
    else:
        for chat_context in CHAT_CONTEXT_LIST:
            chat_context.append_tool_message(index, content)


def start_chat(round_number: int = 0, init_message: str | None = None) -> None:
    if init_message is not None and len(init_message) > 0:
        insert_message(None, RoleType.USER, init_message)
    current_chat_index: int = 0
    for chat_context in get_chat_context(round_number):
        current_chat_index = current_chat_index + 1
        chat_info: str = f"对话轮次-{current_chat_index}，对话节点id：{chat_context.get_index()}，模型：{chat_context.get_model_name()}"
        print(Fore.BLUE + f"{chat_info}\n" + Style.RESET_ALL)
        LOGGER.info(chat_info)
        need_next_chat: bool = True
        while need_next_chat:
            need_next_chat = False
            current_thinking: str = ""
            current_content: str = ""
            is_thinking: bool = True
            for current_message in chat_context.stream_response():
                if current_message.type == MessageType.THINKING:
                    message_thinking: str = current_message.content.replace("\n", "")
                    print(Fore.LIGHTBLACK_EX + message_thinking + Style.RESET_ALL, end="")
                    current_thinking += message_thinking
                    is_thinking = True
                else:
                    if is_thinking:
                        print("\n")
                    if current_message.type == MessageType.TOOL_CALL:
                        tool_calls_info: List[dict] = current_message.content
                        insert_message(chat_context.get_index(), RoleType.ASSISTANT, JsonUtil.to_json(tool_calls_info))
                        print("请求方法：", tool_calls_info)
                        LOGGER.info(f"请求方法：{JsonUtil.to_json(tool_calls_info).replace("\n", "\\n")}")
                        for tool_call_info in tool_calls_info:
                            function_result: str = LlmFunctionManager.execute(tool_call_info["function"]["name"], tool_call_info["function"]["arguments"])
                            print("返回值：", function_result)
                            LOGGER.info(f"返回值：{function_result.replace("\n", "\\n")}")
                            insert_message(chat_context.get_index(), RoleType.TOOL, function_result, tool_call_info["function"]["index"])
                        need_next_chat = True
                    elif current_message.type == MessageType.CONTENT:
                        message_content: str = current_message.content
                        current_content: str = current_content + message_content
                        print(message_content, end="")
                    is_thinking = False
            print("\n")
            LOGGER.info(f"思考内容：{current_thinking.replace("\n", "\\n")}")
            LOGGER.info(f"输出内容：{current_content.replace("\n", "\\n")}")
            insert_message(chat_context.get_index(), RoleType.ASSISTANT, current_content)


if __name__ == "__main__":
    start_chat(0)
