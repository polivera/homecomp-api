from dataclasses import dataclass

from app.shared.domain.value_objects import SharedAccountID


@dataclass(frozen=True)
class ReminderPayAccountID(SharedAccountID):
    pass
