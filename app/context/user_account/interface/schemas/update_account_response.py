from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateAccountResponse:
    account_id: int
    message: str
