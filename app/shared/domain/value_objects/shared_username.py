from dataclasses import dataclass


@dataclass(frozen=True)
class SharedUsername:
    value: str
