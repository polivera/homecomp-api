from dataclasses import dataclass, field
from decimal import Decimal
from typing import Self


@dataclass(frozen=True)
class ReminderOccurrenceAmount:
    value: Decimal
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, Decimal):
                raise ValueError(f"ReminderOccurrenceAmount must be a Decimal, got {type(self.value)}")
            if self.value < 0:
                raise ValueError(f"ReminderOccurrenceAmount must be non-negative, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: Decimal) -> Self:
        """Create ReminderOccurrenceAmount from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
