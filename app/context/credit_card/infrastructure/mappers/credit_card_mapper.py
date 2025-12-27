from app.context.user_account.domain.value_objects.currency import Currency

from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO
from app.context.credit_card.domain.value_objects.card_limit import CardLimit
from app.context.credit_card.domain.value_objects.card_used import CardUsed
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)
from app.context.credit_card.infrastructure.models.credit_card_model import (
    CreditCardModel,
)
from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.value_objects.account_id import UserAccountID


class CreditCardMapper:
    """Mapper for converting between CreditCardModel and CreditCardDTO"""

    @staticmethod
    def toDTO(model: CreditCardModel) -> CreditCardDTO:
        """Convert database model to domain DTO"""
        return CreditCardDTO(
            credit_card_id=CreditCardID.from_trusted_source(model.id),
            user_id=UserID(model.user_id),
            account_id=UserAccountID.from_trusted_source(model.account_id),
            name=CreditCardName.from_trusted_source(model.name),
            currency=Currency.from_trusted_source(model.currency),
            limit=CardLimit.from_trusted_source(model.limit),
            used=CardUsed.from_trusted_source(model.used),
        )

    @staticmethod
    def toModel(dto: CreditCardDTO) -> CreditCardModel:
        """Convert domain DTO to database model"""
        return CreditCardModel(
            id=dto.credit_card_id.value if dto.credit_card_id is not None else None,
            user_id=dto.user_id.value,
            account_id=dto.account_id.value,
            name=dto.name.value,
            currency=dto.currency.value,
            limit=dto.limit.value,
            used=dto.used.value,
        )
