from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateAccountResponse:
    """Response schema for account update"""

    account_id: int
    account_name: str
    account_balance: float
