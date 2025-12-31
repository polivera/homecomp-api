from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self


@dataclass(frozen=True)
class EntryDate:
    """Value object for entry date (when the financial transaction occurred)"""

    value: datetime
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        """Validate that entry_date is timezone-aware"""
        if not self._validated:
            if not isinstance(self.value, datetime):
                raise ValueError("EntryDate must be a datetime object")
            if self.value.tzinfo is None:
                raise ValueError("EntryDate must be timezone-aware")

    @classmethod
    def now(cls) -> Self:
        """Create an EntryDate for the current moment (UTC)"""
        return cls(value=datetime.now(UTC), _validated=True)

    @classmethod
    def from_trusted_source(cls, value: datetime) -> Self:
        """Create EntryDate from trusted source (e.g., database) - skips validation"""
        return cls(value=value, _validated=True)
