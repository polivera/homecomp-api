from dataclasses import dataclass, field
from typing import Self

VALID_FREQUENCIES = {"daily", "weekly", "biweekly", "monthly", "quarterly", "yearly"}


@dataclass(frozen=True)
class ReminderFrequency:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, str):
                raise ValueError(f"ReminderFrequency must be a string, got {type(self.value)}")
            if self.value.lower() not in VALID_FREQUENCIES:
                raise ValueError(f"ReminderFrequency must be one of {VALID_FREQUENCIES}, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create ReminderFrequency from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
