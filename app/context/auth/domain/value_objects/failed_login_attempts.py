from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class FailedLoginAttempts:
    value: int
    _max_attempts: int = 4
    _wait_attempts: list[float] = field(default_factory=lambda: [0, 0, 2, 4])

    def hasReachMaxAttempts(self) -> bool:
        return self.value >= self._max_attempts

    def getAttemptDelay(self) -> float:
        return self._wait_attempts[self.value] if self.value < len(self._wait_attempts) else 4

    @classmethod
    def reset(cls) -> Self:
        return cls(0)
