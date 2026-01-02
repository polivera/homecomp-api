from dataclasses import dataclass


@dataclass(frozen=True)
class FindAccountByIdQuery:
    account_id: int
    user_id: int
