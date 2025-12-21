from dataclasses import dataclass


@dataclass(frozen=True)
class FailedLoginAttempts:
    value: int
    _max_attempts: int = 4

    def hasReachMaxAttempts(self) -> bool:
        return self.value >= self._max_attempts
