import enum
import json
from abc import ABC, abstractmethod, ABCMeta
from typing import Any


class Serializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict | list | str | int | float | bool | None:
        pass


class SerializableEnumMeta(ABCMeta, enum.EnumMeta):
    pass


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> dict | list | str | int | float | bool | None:
        if isinstance(obj, str | int | float | bool | None):
            return obj
        if isinstance(obj, Serializable):
            return self.default(obj.to_dict())
        if isinstance(obj, list):
            return [self.default(item) for item in obj]
        if isinstance(obj, dict):
            result: dict = {}
            for key, value in obj.items():
                current_value = self.default(value)
                if current_value is not None:
                    result[self.default(key)] = self.default(value)
            return result
        raise TypeError(f"Unsupported type: {type(obj).__name__}")


def from_json(json_str: str) -> dict | list:
    return json.loads(json_str)


def to_json(obj: Any) -> str:
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, ensure_ascii=False, cls=CustomJsonEncoder)
