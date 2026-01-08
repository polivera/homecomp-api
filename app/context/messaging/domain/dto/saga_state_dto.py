from dataclasses import dataclass

from app.context.messaging.domain.value_objects import SagaID, SagaPayload, SagaStatus, SagaTime, SagaType


@dataclass(frozen=True)
class SagaStateDTO:
    id: SagaID
    type: SagaType
    status: SagaStatus
    payload: SagaPayload
    created_at: SagaTime
    updated_at: SagaTime | None = None
    completed_at: SagaTime | None = None
