from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class SharedCategoryID:
    """Value object for category identifier"""

    value: int
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and not isinstance(self.value, int):
            raise ValueError(f"CategoryID must be an integer, got {type(self.value)}")
        if not self._validated and self.value <= 0:
            raise ValueError(f"CategoryID must be positive, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: int) -> Self:
        """Create CategoryID from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
