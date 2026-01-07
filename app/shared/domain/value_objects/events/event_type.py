"""Event type identifier value object"""

from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class EventType:
    """Type identifier for domain events (used for routing)"""

    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not self.value:
                raise ValueError("Event type cannot be empty")
            if not self.value[0].isupper():
                raise ValueError("Event type must start with uppercase letter")
            if not self.value.endswith("Event"):
                raise ValueError("Event type must end with 'Event'")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create EventType without validation (from database)"""
        return cls(value=value, _validated=True)
