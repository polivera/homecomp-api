from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCreditCardCommand:
    """Command to create a new credit card"""

    user_id: int
    account_id: int
    name: str
    currency: str
    limit: float
