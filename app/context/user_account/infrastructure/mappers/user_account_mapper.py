from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects.account_id import AccountID
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.domain.value_objects.balance import Balance
from app.context.user_account.domain.value_objects.currency import Currency
from app.context.user_account.infrastructure.models.user_account_model import (
    UserAccountModel,
)


class UserAccountMapper:
    """Mapper for converting between UserAccountModel and UserAccountDTO"""

    @staticmethod
    def toDTO(model: UserAccountModel) -> UserAccountDTO:
        """Convert database model to domain DTO"""
        return UserAccountDTO(
            account_id=AccountID.from_trusted_source(model.id),
            user_id=UserID(model.user_id),
            name=AccountName.from_trusted_source(model.name),
            currency=Currency.from_trusted_source(model.currency),
            balance=Balance.from_trusted_source(model.balance),
        )

    @staticmethod
    def toModel(dto: UserAccountDTO) -> UserAccountModel:
        """Convert domain DTO to database model"""
        return UserAccountModel(
            id=dto.account_id.value if dto.account_id is not None else None,
            user_id=dto.user_id.value,
            name=dto.name.value,
            currency=dto.currency.value,
            balance=dto.balance.value,
        )
