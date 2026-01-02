from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateCreditCardCommand:
    """Command to update an existing credit card"""

    credit_card_id: int
    user_id: int
    name: str | None = None
    limit: float | None = None
    used: float | None = None
    currency: str | None = None
