from dataclasses import dataclass, field
from datetime import datetime

from app.shared.domain.value_objects import SharedDateTime


@dataclass(frozen=True)
class EntryDate(SharedDateTime):
    """Value object for entry date (when the financial transaction occurred)"""

    value: datetime
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        """Validate that entry_date is timezone-aware"""
        if not self._validated:
            if not isinstance(self.value, datetime):
                raise ValueError("EntryDate must be a datetime object")
            super().__post_init__()
