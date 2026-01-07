"""Event payload value object"""

from dataclasses import dataclass

from app.shared.domain.value_objects.shared_payload import SharedPayload


@dataclass(frozen=True)
class EventPayload(SharedPayload):
    """Type-safe wrapper for event metadata"""

    pass
