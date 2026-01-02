from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class UserID:
    """User identifier value object"""

    value: int
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and (not isinstance(self.value, int) or self.value <= 0):
            raise ValueError(f"Invalid user ID: {self.value}. Must be a positive integer.")

    @classmethod
    def from_trusted_source(cls, value: int) -> Self:
        """
        Create UserID from trusted source (e.g., database) - skips validation.
        Use this to avoid performance overhead when data is already validated.
        """
        return cls(value, _validated=True)
