from dataclasses import dataclass
from decimal import Decimal

from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO


@dataclass(frozen=True)
class CreditCardResponseDTO:
    """Application layer DTO for credit card responses"""

    credit_card_id: int
    user_id: int
    account_id: int
    name: str
    currency: str
    limit: Decimal
    used: Decimal

    @classmethod
    def from_domain_dto(cls, domain_dto: CreditCardDTO) -> "CreditCardResponseDTO":
        """Convert from domain DTO to application response DTO"""
        return cls(
            credit_card_id=domain_dto.credit_card_id.value,
            user_id=domain_dto.user_id.value,
            account_id=domain_dto.account_id.value,
            name=domain_dto.name.value,
            currency=domain_dto.currency.value,
            limit=domain_dto.limit.value,
            used=domain_dto.used.value,
        )
