
from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.exceptions import HouseholdMapperError
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)
from app.context.household.infrastructure.models import HouseholdModel


class HouseholdMapper:
    @staticmethod
    def to_dto(model: HouseholdModel | None) -> HouseholdDTO | None:
        """Convert database model to domain DTO"""
        if model is None:
            return None

        try:
            return HouseholdDTO(
                household_id=HouseholdID(model.id),
                owner_user_id=HouseholdUserID(model.owner_user_id),
                name=HouseholdName.from_trusted_source(model.name),
                created_at=model.created_at,
            )
        except Exception as e:
            raise HouseholdMapperError(
                f"Error mapping HouseholdModel to DTO: {e}"
            ) from e

    @staticmethod
    def to_dto_or_fail(model: HouseholdModel | None) -> HouseholdDTO:
        dto = HouseholdMapper.to_dto(model)
        if not dto:
            raise HouseholdMapperError("Error mapping HouseholdModel to DTO")
        return dto

    @staticmethod
    def to_model(dto: HouseholdDTO) -> HouseholdModel:
        """Convert domain DTO to database model"""
        try:
            model = HouseholdModel(
                owner_user_id=dto.owner_user_id.value,
                name=dto.name.value,
            )

            if dto.household_id is not None:
                model.id = dto.household_id.value

            if dto.created_at is not None:
                model.created_at = dto.created_at

            return model
        except Exception as e:
            raise HouseholdMapperError(
                f"Error mapping HouseholdDTO to model: {e}"
            ) from e
