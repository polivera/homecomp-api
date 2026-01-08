from dataclasses import dataclass

from app.shared.domain.value_objects import SharedPayload


@dataclass(frozen=True)
class EventPayload(SharedPayload):
    pass
