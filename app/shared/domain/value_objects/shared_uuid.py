import uuid
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class SharedUUID:
    value: str

    @classmethod
    def generate(cls) -> Self:
        return cls(value=str(uuid.uuid4))

    @classmethod
    def from_trusted_source(cls, uuid: str) -> Self:
        return cls
