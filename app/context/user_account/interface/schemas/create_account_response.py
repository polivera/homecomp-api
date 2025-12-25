from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAccountResponse:
    """Response schema for account creation"""

    account_id: int
    account_name: str
    message: str
