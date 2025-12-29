
from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.exceptions import UserAccountMapperError
from app.context.user_account.domain.value_objects import (
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountDeletedAt,
    UserAccountUserID,
)
from app.context.user_account.domain.value_objects.account_id import UserAccountID
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.infrastructure.models.user_account_model import (
    UserAccountModel,
)


class UserAccountMapper:
    """Mapper for converting between UserAccountModel and UserAccountDTO"""

    @staticmethod
    def to_dto(model: UserAccountModel | None) -> UserAccountDTO | None:
        """Convert database model to domain DTO"""
        return (
            UserAccountDTO(
                account_id=UserAccountID.from_trusted_source(model.id),
                user_id=UserAccountUserID.from_trusted_source(model.user_id),
                name=AccountName.from_trusted_source(model.name),
                currency=UserAccountCurrency.from_trusted_source(model.currency),
                balance=UserAccountBalance.from_trusted_source(model.balance),
                deleted_at=UserAccountDeletedAt.from_optional(model.deleted_at),
            )
            if model
            else None
        )

    @staticmethod
    def to_dto_or_fail(model: UserAccountModel) -> UserAccountDTO:
        dto = UserAccountMapper.to_dto(model)
        if dto is None:
            raise UserAccountMapperError("User account dto cannot be null")
        return dto

    @staticmethod
    def to_model(dto: UserAccountDTO) -> UserAccountModel:
        """Convert domain DTO to database model"""
        return UserAccountModel(
            id=dto.account_id.value if dto.account_id is not None else None,
            user_id=dto.user_id.value,
            name=dto.name.value,
            currency=dto.currency.value,
            balance=dto.balance.value,
            deleted_at=dto.deleted_at.value if dto.deleted_at is not None else None,
        )
