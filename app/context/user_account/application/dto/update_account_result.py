from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateAccountResult:
    account_id: int
    message: str
