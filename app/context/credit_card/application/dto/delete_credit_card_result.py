from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DeleteCreditCardErrorCode(str, Enum):
    """Error codes for credit card deletion"""

    NOT_FOUND = "NOT_FOUND"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class DeleteCreditCardResult:
    """Result of credit card deletion operation"""

    success: bool = False
    error_code: Optional[DeleteCreditCardErrorCode] = None
    error_message: Optional[str] = None
