import enum
from dataclasses import dataclass
from typing import List

from python.cbb import JsonUtil
from python.cbb.JsonUtil import Serializable, SerializableEnumMeta


class MessageType(Serializable, enum.Enum, metaclass=SerializableEnumMeta):
    TOOL_CALL = (0, "tool_calls")
    THINKING = (1, "thinking")
    CONTENT = (2, "content")

    __index: int
    __key: str

    def __init__(self, index: int, key: str):
        self.__index = index
        self.__key = key

    def get_index(self) -> int:
        return self.__index

    def get_key(self) -> str:
        return self.__key

    def to_dict(self) -> str:
        return self.get_key()


@dataclass
class TypedResponseMessage(Serializable):
    type: MessageType
    content: str | List[dict]

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "content": self.content,
        }


class RoleType(Serializable, enum.Enum, metaclass=SerializableEnumMeta):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    TOOL = "tool"

    def to_dict(self) -> str:
        return JsonUtil.to_json(self.value)


@dataclass
class TypedContextMessage(Serializable):
    role: RoleType
    content: str
    index: int | None

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "index": self.index,
        }


@dataclass
class OllamaRequestBody(Serializable):
    model: str
    messages: List[TypedContextMessage]
    tools: List[dict]
    stream: bool

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "messages": self.messages,
            "tools": self.tools,
            "stream": self.stream,
        }


if __name__ == '__main__':
    print(JsonUtil.to_json(TypedContextMessage(RoleType.SYSTEM, "123", None)))
