from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAccountCommand:
    """Command to create a new user account"""

    user_id: int
    name: str
    currency: str
    balance: float
