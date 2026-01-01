from app.context.reminder.domain.dto import ReminderOccurrenceDTO
from app.context.reminder.domain.value_objects import (
    ReminderID,
    ReminderOccurrenceAmount,
    ReminderOccurrenceID,
    ReminderOccurrenceScheduledDate,
    ReminderOccurrenceStatus,
)
from app.context.reminder.infrastructure.models import ReminderOccurrenceModel


class ReminderOccurrenceMapper:
    """Mapper for converting between ReminderOccurrenceModel and ReminderOccurrenceDTO"""

    @staticmethod
    def to_dto(model: ReminderOccurrenceModel | None) -> ReminderOccurrenceDTO | None:
        """Convert database model to domain DTO"""
        return (
            ReminderOccurrenceDTO(
                occurrence_id=ReminderOccurrenceID.from_trusted_source(model.id),
                reminder_id=ReminderID.from_trusted_source(model.reminder_id),
                scheduled_date=ReminderOccurrenceScheduledDate.from_trusted_source(model.scheduled_date),
                amount=ReminderOccurrenceAmount.from_trusted_source(model.amount),
                status=ReminderOccurrenceStatus(model.status),
                entry_id=model.entry_id,
            )
            if model
            else None
        )

    @staticmethod
    def to_dto_or_fail(model: ReminderOccurrenceModel) -> ReminderOccurrenceDTO:
        """Convert database model to domain DTO, raising error if model is None"""
        dto = ReminderOccurrenceMapper.to_dto(model)
        if dto is None:
            raise ValueError("Reminder occurrence DTO cannot be null")
        return dto

    @staticmethod
    def to_model(dto: ReminderOccurrenceDTO) -> ReminderOccurrenceModel:
        """Convert domain DTO to database model"""
        return ReminderOccurrenceModel(
            id=dto.occurrence_id.value if dto.occurrence_id is not None else None,
            reminder_id=dto.reminder_id.value,
            scheduled_date=dto.scheduled_date.value,
            amount=dto.amount.value,
            status=dto.status.value,
            entry_id=dto.entry_id,
        )
