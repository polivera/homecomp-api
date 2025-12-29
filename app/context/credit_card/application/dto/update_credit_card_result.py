from dataclasses import dataclass
from enum import Enum


class UpdateCreditCardErrorCode(str, Enum):
    """Error codes for credit card update"""

    NOT_FOUND = "NOT_FOUND"
    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class UpdateCreditCardResult:
    """Result of credit card update operation"""

    # Success fields - populated when operation succeeds
    credit_card_id: int | None = None
    credit_card_name: str | None = None

    # Error fields - populated when operation fails
    error_code: UpdateCreditCardErrorCode | None = None
    error_message: str | None = None
