from dataclasses import dataclass


@dataclass(frozen=True)
class UserID:
    value: int
