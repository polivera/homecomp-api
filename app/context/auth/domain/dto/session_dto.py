from dataclasses import dataclass

from app.context.auth.domain.value_objects import (
    AuthUserID,
    FailedLoginAttempts,
    SessionToken,
)
from app.context.auth.domain.value_objects.blocked_time import BlockedTime


@dataclass(frozen=True)
class SessionDTO:
    user_id: AuthUserID
    token: SessionToken | None
    failed_attempts: FailedLoginAttempts
    blocked_until: BlockedTime | None
