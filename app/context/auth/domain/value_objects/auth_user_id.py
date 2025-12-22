from dataclasses import dataclass


@dataclass(frozen=True)
class AuthUserID:
    value: int
