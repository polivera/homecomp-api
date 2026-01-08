from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class SagaType:
    value: str

    @classmethod
    def from_trusted_source(cls, type: str) -> Self:
        return cls(value=type)
