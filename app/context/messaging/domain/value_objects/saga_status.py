from dataclasses import dataclass
from enum import Enum
from typing import Self


class SagaStatusEnum(str, Enum):
    PENDING = "pending"
    INITIATED = "initiated"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"


@dataclass(frozen=True)
class SagaStatus:
    value: str

    @classmethod
    def from_trusted_source(cls, status: str) -> Self:
        return cls(value=status)
