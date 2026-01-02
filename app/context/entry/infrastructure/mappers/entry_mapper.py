from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import EntryMapperError
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryAmount,
    EntryCategoryID,
    EntryDate,
    EntryDescription,
    EntryHouseholdID,
    EntryID,
    EntryType,
    EntryUserID,
)
from app.context.entry.infrastructure.models import EntryModel


class EntryMapper:
    """Mapper for converting between EntryModel and EntryDTO"""

    @staticmethod
    def to_dto(model: EntryModel | None) -> EntryDTO | None:
        """Convert database model to domain DTO"""
        return (
            EntryDTO(
                entry_id=EntryID.from_trusted_source(model.id),
                user_id=EntryUserID.from_trusted_source(model.user_id),
                account_id=EntryAccountID.from_trusted_source(model.account_id),
                category_id=EntryCategoryID.from_trusted_source(model.category_id),
                entry_type=EntryType.from_trusted_source(model.entry_type),
                entry_date=EntryDate.from_trusted_source(model.entry_date),
                amount=EntryAmount.from_trusted_source(model.amount),
                description=EntryDescription.from_trusted_source(model.description),
                household_id=(
                    EntryHouseholdID.from_trusted_source(model.household_id) if model.household_id is not None else None
                ),
            )
            if model
            else None
        )

    @staticmethod
    def to_dto_or_fail(model: EntryModel) -> EntryDTO:
        """Convert model to DTO or raise exception"""
        dto = EntryMapper.to_dto(model)
        if dto is None:
            raise EntryMapperError("Entry DTO cannot be null")
        return dto

    @staticmethod
    def to_model(dto: EntryDTO) -> EntryModel:
        """Convert domain DTO to database model"""
        return EntryModel(
            id=dto.entry_id.value if dto.entry_id is not None else None,
            user_id=dto.user_id.value,
            account_id=dto.account_id.value,
            category_id=dto.category_id.value,
            entry_type=dto.entry_type.value,
            entry_date=dto.entry_date.value,
            amount=dto.amount.value,
            description=dto.description.value,
            household_id=dto.household_id.value if dto.household_id is not None else None,
        )
