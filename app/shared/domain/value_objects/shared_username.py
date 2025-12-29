from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class SharedUsername:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create Balance from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
