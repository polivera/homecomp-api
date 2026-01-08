from dataclasses import dataclass

from app.context.messaging.domain.dto import SagaStateDTO
from app.context.messaging.domain.value_objects import SagaID, SagaPayload, SagaStatus, SagaTime, SagaType
from app.context.messaging.infrastructure.models import SagaStateModel


@dataclass(frozen=True)
class SagaMapper:
    @classmethod
    def to_model(cls, dto: SagaStateDTO) -> SagaStateModel:
        return SagaStateModel(
            saga_id=dto.id.value,
            saga_type=dto.type.value,
            status=dto.status.value,
            payload=dto.payload.value,
            created_at=dto.created_at.value,
            updated_at=dto.updated_at.value if dto.updated_at else None,
            completed_at=dto.completed_at.value if dto.completed_at else None,
        )

    @classmethod
    def to_dto(cls, model: SagaStateModel) -> SagaStateDTO:
        return SagaStateDTO(
            id=SagaID.from_trusted_source(model.saga_id),
            type=SagaType.from_trusted_source(model.saga_type),
            status=SagaStatus.from_trusted_source(model.status),
            payload=SagaPayload.from_trusted_source(model.payload),
            created_at=SagaTime.from_trusted_source(model.created_at),
            updated_at=SagaTime.from_trusted_source(model.updated_at),
            completed_at=SagaTime.from_trusted_source(model.updated_at),
        )
