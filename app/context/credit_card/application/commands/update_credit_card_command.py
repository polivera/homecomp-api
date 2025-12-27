from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UpdateCreditCardCommand:
    """Command to update an existing credit card"""

    credit_card_id: int
    user_id: int
    name: Optional[str] = None
    limit: Optional[float] = None
    used: Optional[float] = None
    currency: Optional[str] = None
