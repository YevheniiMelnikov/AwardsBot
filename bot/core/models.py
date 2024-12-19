from dataclasses import dataclass
from typing import Type, TypeVar, Any

T = TypeVar("T", bound="BaseEntity")


@dataclass
class BaseEntity:
    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
        fields = {field.name for field in cls.__dataclass_fields__.values()}
        filtered_data = {key: data.get(key) for key in fields if key in data}
        return cls(**filtered_data)

    def to_dict(self) -> dict[str, Any]:
        return {field.name: getattr(self, field.name) for field in self.__dataclass_fields__.values()}

    def __repr__(self) -> str:
        field_str = ", ".join(f"{name}={getattr(self, name)!r}" for name in self.__dataclass_fields__)
        return f"{self.__class__.__name__}({field_str})"


@dataclass
class User(BaseEntity):
    tg_id: int
    username: str
