from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self


@dataclass(frozen=True)
class SharedDateTime:
    value: datetime
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            # Rule 1: Must be timezone-aware
            if self.value.tzinfo is None:
                raise ValueError(
                    f"{self.__class__.__name__} must be timezone-aware. "
                    "Naive datetimes are rejected."
                )

            # Rule 2: Convert to UTC (normalize)
            if self.value.tzinfo != UTC:
                utc_value = self.value.astimezone(UTC)
                object.__setattr__(self, "value", utc_value)

    @classmethod
    def from_trusted_source(cls, value: datetime) -> Self:
        """Skip validation - for database reads"""
        return cls(value=value, _validated=True)
