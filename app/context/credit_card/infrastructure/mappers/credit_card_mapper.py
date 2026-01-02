from app.context.credit_card.domain.dto import CreditCardDTO
from app.context.credit_card.domain.exceptions import CreditCardMapperError
from app.context.credit_card.domain.value_objects import (
    CardLimit,
    CardUsed,
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardDeletedAt,
    CreditCardID,
    CreditCardName,
    CreditCardUserID,
)
from app.context.credit_card.infrastructure.models import CreditCardModel


class CreditCardMapper:
    """Mapper for converting between CreditCardModel and CreditCardDTO"""

    @staticmethod
    def to_dto(model: CreditCardModel | None) -> CreditCardDTO | None:
        """Convert database model to domain DTO"""
        return (
            CreditCardDTO(
                credit_card_id=CreditCardID.from_trusted_source(model.id),
                user_id=CreditCardUserID(model.user_id),
                account_id=CreditCardAccountID.from_trusted_source(model.account_id),
                name=CreditCardName.from_trusted_source(model.name),
                currency=CreditCardCurrency.from_trusted_source(model.currency),
                limit=CardLimit.from_trusted_source(model.limit),
                used=CardUsed.from_trusted_source(model.used),
                deleted_at=CreditCardDeletedAt.from_optional(model.deleted_at),
            )
            if model
            else None
        )

    @staticmethod
    def to_dto_or_fail(model: CreditCardModel) -> CreditCardDTO:
        """Convert database model to domain DTO, raising error if model is None"""
        dto = CreditCardMapper.to_dto(model)
        if dto is None:
            raise CreditCardMapperError("Credit card dto cannot be null")
        return dto

    @staticmethod
    def to_model(dto: CreditCardDTO) -> CreditCardModel:
        """Convert domain DTO to database model"""
        return CreditCardModel(
            id=dto.credit_card_id.value if dto.credit_card_id is not None else None,
            user_id=dto.user_id.value,
            account_id=dto.account_id.value,
            name=dto.name.value,
            currency=dto.currency.value,
            limit=dto.limit.value,
            used=dto.used.value if dto.used is not None else 0,
            deleted_at=dto.deleted_at.value if dto.deleted_at is not None else None,
        )
