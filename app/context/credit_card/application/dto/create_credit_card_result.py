from dataclasses import dataclass
from enum import Enum


class CreateCreditCardErrorCode(str, Enum):
    """Error codes for credit card creation"""

    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateCreditCardResult:
    """Result of credit card creation operation"""

    # Success fields - populated when operation succeeds
    credit_card_id: int | None = None

    # Error fields - populated when operation fails
    error_code: CreateCreditCardErrorCode | None = None
    error_message: str | None = None
