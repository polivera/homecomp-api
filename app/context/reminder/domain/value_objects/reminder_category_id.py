from dataclasses import dataclass

from app.shared.domain.value_objects import SharedCategoryID


@dataclass(frozen=True)
class ReminderCategoryID(SharedCategoryID):
    pass
