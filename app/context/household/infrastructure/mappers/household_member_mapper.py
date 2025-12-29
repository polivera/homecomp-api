from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.exceptions import HouseholdMapperError
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdName,
    HouseholdRole,
    HouseholdUserID,
)
from app.context.household.domain.value_objects.household_user_name import (
    HouseholdUserName,
)
from app.context.household.infrastructure.models import (
    HouseholdMemberModel,
    HouseholdModel,
)
from app.context.user.infrastructure.models import UserModel


class HouseholdMemberMapper:
    """Mapper for converting between HouseholdMemberModel and HouseholdMemberDTO"""

    @staticmethod
    def to_dto(
        model: HouseholdMemberModel,
        household_model: HouseholdModel | None = None,
        user_model: UserModel | None = None,
    ) -> HouseholdMemberDTO:
        """Convert database model to domain DTO"""
        return HouseholdMemberDTO(
            member_id=HouseholdMemberID(model.id),
            household_id=HouseholdID(model.household_id),
            user_id=HouseholdUserID(model.user_id),
            role=HouseholdRole.from_trusted_source(model.role),
            joined_at=model.joined_at,
            invited_by_user_id=(
                HouseholdUserID(model.invited_by_user_id) if model.invited_by_user_id is not None else None
            ),
            invited_at=model.invited_at,
            household_name=(HouseholdName(household_model.name) if household_model else None),
            inviter_username=(HouseholdUserName(user_model.username or user_model.email) if user_model else None),
        )

    @staticmethod
    def to_model(dto: HouseholdMemberDTO) -> HouseholdMemberModel:
        """Convert domain DTO to database model"""
        return HouseholdMemberModel(
            id=dto.member_id.value if dto.member_id else None,
            household_id=dto.household_id.value,
            user_id=dto.user_id.value,
            role=dto.role.value,
            joined_at=dto.joined_at,
            invited_by_user_id=(dto.invited_by_user_id.value if dto.invited_by_user_id else None),
            invited_at=dto.invited_at,
        )

    @staticmethod
    def to_dto_or_fail(model: HouseholdMemberModel) -> HouseholdMemberDTO:
        """Convert model to DTO, raise HouseholdMapperError if fails"""
        try:
            return HouseholdMemberMapper.to_dto(model)
        except Exception as e:
            raise HouseholdMapperError(f"Failed to map model to DTO: {str(e)}") from Exception
