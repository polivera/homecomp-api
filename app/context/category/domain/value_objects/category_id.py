from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class CategoryID:
    """Value object for category ID"""

    value: int
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and (not isinstance(self.value, int) or self.value <= 0):
            raise ValueError(f"CategoryID must be a positive integer, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: int) -> Self:
        """Create CategoryID from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
