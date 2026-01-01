from dataclasses import dataclass

from app.shared.domain.value_objects import SharedDateTime


@dataclass(frozen=True)
class ReminderEndDate(SharedDateTime):
    pass
