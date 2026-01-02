from dataclasses import dataclass


@dataclass(frozen=True)
class FindAccountsByUserQuery:
    user_id: int
