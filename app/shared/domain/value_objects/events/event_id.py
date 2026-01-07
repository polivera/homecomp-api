"""Event identifier value object"""

from dataclasses import dataclass

from app.shared.domain.value_objects.shared_uuid import SharedUUID


@dataclass(frozen=True)
class EventId(SharedUUID):
    """Unique identifier for domain events across all contexts"""

    pass
