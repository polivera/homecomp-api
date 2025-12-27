from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CreateCreditCardErrorCode(str, Enum):
    """Error codes for credit card creation"""

    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateCreditCardResult:
    """Result of credit card creation operation"""

    # Success fields - populated when operation succeeds
    credit_card_id: Optional[int] = None

    # Error fields - populated when operation fails
    error_code: Optional[CreateCreditCardErrorCode] = None
    error_message: Optional[str] = None
