from dataclasses import dataclass, field
from typing import Self

VALID_STATUSES = {"pending", "completed", "cancelled"}


@dataclass(frozen=True)
class ReminderOccurrenceStatus:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, str):
                raise ValueError(f"ReminderOccurrenceStatus must be a string, got {type(self.value)}")
            if self.value.lower() not in VALID_STATUSES:
                raise ValueError(f"ReminderOccurrenceStatus must be one of {VALID_STATUSES}, got {self.value}")

    @property
    def is_pending(self) -> bool:
        return self.value.lower() == "pending"

    @property
    def is_completed(self) -> bool:
        return self.value.lower() == "completed"

    @property
    def is_cancelled(self) -> bool:
        return self.value.lower() == "cancelled"

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create ReminderOccurrenceStatus from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
