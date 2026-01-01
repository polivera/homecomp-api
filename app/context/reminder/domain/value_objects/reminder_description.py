from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class ReminderDescription:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, str):
                raise ValueError(f"ReminderDescription must be a string, got {type(self.value)}")
            if len(self.value) > 500:
                raise ValueError(f"ReminderDescription must be <= 500 characters, got {len(self.value)}")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create ReminderDescription from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
