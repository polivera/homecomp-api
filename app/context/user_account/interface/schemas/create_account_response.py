from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAccountResponse:
    """Response schema for account creation"""

    account_id: int | None
    account_name: str | None
    account_balance: float | None
