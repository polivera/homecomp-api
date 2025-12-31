from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self

from app.shared.domain.value_objects import SharedYear
from app.shared.domain.value_objects.shared_month import SharedMonth


@dataclass(frozen=True)
class SharedDateTime:
    value: datetime
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            # Rule 1: Must be timezone-aware
            if self.value.tzinfo is None:
                raise ValueError(f"{self.__class__.__name__} must be timezone-aware. Naive datetimes are rejected.")

            # Rule 2: Convert to UTC (normalize)
            if self.value.tzinfo != UTC:
                utc_value = self.value.astimezone(UTC)
                object.__setattr__(self, "value", utc_value)

    @classmethod
    def from_trusted_source(cls, value: datetime) -> Self:
        """Skip validation - for database reads"""
        return cls(value=value, _validated=True)

    @classmethod
    def now(cls) -> Self:
        """Create an EntryDate for the current moment (UTC)"""
        return cls(value=datetime.now(UTC), _validated=True)

    @classmethod
    def start_of_month(cls, month: SharedMonth, year: SharedYear) -> Self:
        """Get the first moment of the specified month"""
        return cls(value=datetime(year.value, month.value, 1, tzinfo=UTC), _validated=True)

    @classmethod
    def start_of_next_month(cls, month: SharedMonth, year: SharedYear) -> Self:
        """Get the first moment of the next month (handles year rollover)"""
        if month.value == 12:
            next_month = 1
            next_year = year.value + 1
        else:
            next_month = month.value + 1
            next_year = year.value

        return cls(value=datetime(next_year, next_month, 1, tzinfo=UTC), _validated=True)
