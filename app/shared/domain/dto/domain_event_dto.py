"""
Domain Event DTO

Events are immutable data structures representing things that happened in the domain.
They carry information about the event but have no behavior.

All context-specific events should extend this base DTO.
"""

from abc import ABC
from dataclasses import dataclass

from app.shared.domain.value_objects.events import EventId, EventPayload, EventType, OccurredAt


@dataclass(frozen=True)
class DomainEventDTO(ABC):
    """
    Base DTO for all domain events.

    Events are data containers representing domain occurrences.
    Use ABC to prevent direct instantiation - always subclass.

    Uses value objects for type safety:
    - EventId: Validated UUID for unique event identification
    - OccurredAt: Validated UTC datetime for when event occurred
    - EventType: Event type identifier for routing
    - EventPayload: Flexible dict for additional metadata
    """

    event_id: EventId
    occurred_at: OccurredAt
    event_type: EventType
    payload: EventPayload
