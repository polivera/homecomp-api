from dataclasses import dataclass

from app.context.auth.domain.value_objects import FailedLoginAttempts


@dataclass(frozen=True)
class ThrottleTime:
    value: int
    _throttleTimeSeconds = tuple[int, ...] = (0, 2, 4, 8)

    @classmethod
    def fromAttempts(cls, attempts: FailedLoginAttempts) -> "ThrottleTime":
        return cls(value=cls._throttleTimeSeconds[attempts.value])
