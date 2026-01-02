from dataclasses import dataclass


@dataclass(frozen=True)
class GetSessionResultDTO:
    user_id: int
    token: str | None
    failed_attempts: int
    blocked_until: str | None
