from dataclasses import dataclass


@dataclass(frozen=True)
class FindUserQuery:
    user_id: int | None = None
    email: str | None = None
