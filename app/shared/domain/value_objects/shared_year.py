from dataclasses import dataclass


@dataclass(frozen=True)
class SharedYear:
    value: int
