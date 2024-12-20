from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T", bound="BaseEntity")


@dataclass
class BaseEntity:
    def to_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.__annotations__.keys()}

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(**{key: data[key] for key in data.keys() if key in cls.__annotations__})

    def __repr__(self) -> str:
        field_str = ", ".join(f"{name}={getattr(self, name)!r}" for name in self.__dataclass_fields__)
        return f"{self.__class__.__name__}({field_str})"


@dataclass
class User(BaseEntity):
    tg_id: int
    username: str


@dataclass
class Candidate(BaseEntity):
    username: str
    nominations: list["CandidateNomination"] = field(default_factory=list)

    def total_votes(self) -> int:
        return sum(nomination.votes for nomination in self.nominations)


@dataclass
class Nomination(BaseEntity):
    name: str
    candidates: list["CandidateNomination"] = field(default_factory=list)
    winner: "Candidate" = None


@dataclass
class CandidateNomination(BaseEntity):
    candidate: Candidate
    nomination: Nomination
    votes: int = 0
