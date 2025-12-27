from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateAccountCommand:
    account_id: int
    user_id: int
    name: str
    currency: str
    balance: float
