from app.context.reminder.domain.dto import ReminderDTO
from app.context.reminder.domain.value_objects import (
    ReminderCategoryID,
    ReminderCurrency,
    ReminderDescription,
    ReminderEndDate,
    ReminderEntryType,
    ReminderFrequency,
    ReminderID,
    ReminderOccurrenceAmount,
    ReminderStartDate,
    ReminderUserID,
)
from app.context.reminder.infrastructure.models import ReminderModel


class ReminderMapper:
    """Mapper for converting between ReminderModel and ReminderDTO"""

    @staticmethod
    def to_dto(model: ReminderModel | None) -> ReminderDTO | None:
        """Convert database model to domain DTO"""
        return (
            ReminderDTO(
                reminder_id=ReminderID.from_trusted_source(model.id),
                user_id=ReminderUserID.from_trusted_source(model.user_id),
                category_id=ReminderCategoryID.from_trusted_source(model.category_id),
                entry_type=ReminderEntryType.from_trusted_source(model.entry_type),
                currency=ReminderCurrency.from_trusted_source(model.currency),
                amount=ReminderOccurrenceAmount.from_trusted_source(model.amount),
                frequency=ReminderFrequency.from_trusted_source(model.frequency),
                start_date=ReminderStartDate.from_trusted_source(model.start_date),
                end_date=ReminderEndDate.from_trusted_source(model.end_date) if model.end_date else None,
                description=ReminderDescription.from_trusted_source(model.description),
            )
            if model
            else None
        )

    @staticmethod
    def to_dto_or_fail(model: ReminderModel) -> ReminderDTO:
        """Convert database model to domain DTO, raising error if model is None"""
        dto = ReminderMapper.to_dto(model)
        if dto is None:
            raise ValueError("Reminder DTO cannot be null")
        return dto

    @staticmethod
    def to_model(dto: ReminderDTO) -> ReminderModel:
        """Convert domain DTO to database model"""
        return ReminderModel(
            id=dto.reminder_id.value if dto.reminder_id is not None else None,
            user_id=dto.user_id.value,
            entry_type=dto.entry_type.value,
            currency=dto.currency.value,
            amount=dto.amount.value,
            frequency=dto.frequency.value,
            start_date=dto.start_date.value,
            category_id=dto.category_id.value,
            description=dto.description.value,
            end_date=dto.end_date.value if dto.end_date else None,
        )
