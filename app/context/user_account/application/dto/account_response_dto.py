from dataclasses import dataclass
from decimal import Decimal

from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO


@dataclass(frozen=True)
class AccountResponseDTO:
    """Application layer DTO for account responses"""

    account_id: int
    user_id: int
    name: str
    currency: str
    balance: Decimal

    @classmethod
    def from_domain_dto(cls, domain_dto: UserAccountDTO) -> "AccountResponseDTO":
        return cls(
            account_id=domain_dto.account_id.value,
            user_id=domain_dto.user_id.value,
            name=domain_dto.name.value,
            currency=domain_dto.currency.value,
            balance=domain_dto.balance.value,
        )
