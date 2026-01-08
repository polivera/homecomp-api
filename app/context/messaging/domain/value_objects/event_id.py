from dataclasses import dataclass

from app.shared.domain.value_objects import SharedUUID


@dataclass(frozen=True)
class EventID(SharedUUID):
    pass
