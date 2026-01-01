from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class ReminderUserID:
    value: int
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, int):
                raise ValueError(f"ReminderUserID must be an integer, got {type(self.value)}")
            if self.value < 1:
                raise ValueError(f"ReminderUserID must be positive, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: int) -> Self:
        """Create ReminderUserID from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
