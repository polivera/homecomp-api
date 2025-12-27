from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteAccountCommand:
    account_id: int
    user_id: int
