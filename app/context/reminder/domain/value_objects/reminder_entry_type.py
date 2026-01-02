from dataclasses import dataclass

from app.shared.domain.value_objects import SharedEntryType


@dataclass(frozen=True)
class ReminderEntryType(SharedEntryType):
    pass
