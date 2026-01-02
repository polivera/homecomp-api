from dataclasses import dataclass


@dataclass(frozen=True)
class GetSessionQuery:
    user_id: int | None = None
    token: str | None = None
