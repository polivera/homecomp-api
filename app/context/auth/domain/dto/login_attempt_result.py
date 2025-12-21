from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LoginAttemptResult:
    is_blocked: bool
    throttle_applied_seconds: int
    attempts_remaining: int
    unblock_at: datetime | None = None
