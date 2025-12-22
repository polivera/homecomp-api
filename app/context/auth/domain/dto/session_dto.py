from dataclasses import dataclass
from typing import Optional

from app.context.auth.domain.value_objects import (
    AuthUserID,
    FailedLoginAttempts,
    SessionToken,
)
from app.context.auth.domain.value_objects.blocked_time import BlockedTime


@dataclass(frozen=True)
class SessionDTO:
    user_id: AuthUserID
    token: Optional[SessionToken]
    failed_attempts: FailedLoginAttempts
    blocked_until: Optional[BlockedTime]
