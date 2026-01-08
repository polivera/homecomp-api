from dataclasses import dataclass

from app.context.messaging.domain.value_objects import (
    EventID,
    EventPayload,
    EventTime,
    EventType,
    SagaID,
)


@dataclass(frozen=True)
class EventMessageDTO:
    event_id: EventID  # UUID - unique identifier
    event_type: EventType  # "PayReminderInitiatedEvent"
    saga_id: SagaID  # UUID - groups events into a saga
    timestamp: EventTime  # When it was created
    payload: EventPayload  # Event-specific data
