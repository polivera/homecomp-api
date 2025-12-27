from dataclasses import dataclass
from enum import Enum
from typing import Optional


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
    credit_card_id: Optional[int] = None
    credit_card_name: Optional[str] = None

    # Error fields - populated when operation fails
    error_code: Optional[UpdateCreditCardErrorCode] = None
    error_message: Optional[str] = None
