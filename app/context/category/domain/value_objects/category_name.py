from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class CategoryName:
    """Value object for category name"""

    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and not isinstance(self.value, str):
            raise ValueError(f"CategoryName must be a string, got {type(self.value)}")
        if not self._validated and not self.value.strip():
            raise ValueError("CategoryName cannot be empty or whitespace")
        if not self._validated and len(self.value) > 100:
            raise ValueError(f"CategoryName cannot exceed 100 characters, got {len(self.value)}")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create CategoryName from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
