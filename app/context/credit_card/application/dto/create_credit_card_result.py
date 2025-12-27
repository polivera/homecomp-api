from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateCreditCardResult:
    """Result of credit card creation operation"""

    credit_card_id: Optional[int] = None
    error: Optional[str] = None
