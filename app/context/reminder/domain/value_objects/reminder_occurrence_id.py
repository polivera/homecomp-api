from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class ReminderOccurrenceID:
    value: int
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, int):
                raise ValueError(f"ReminderOccurrenceID must be an integer, got {type(self.value)}")
            if self.value < 1:
                raise ValueError(f"ReminderOccurrenceID must be positive, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: int) -> Self:
        """Create ReminderOccurrenceID from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
