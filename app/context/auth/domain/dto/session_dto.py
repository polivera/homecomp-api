from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.context.auth.domain.value_objects import (
    AuthUserID,
    FailedLoginAttempts,
    SessionToken,
)


@dataclass(frozen=True)
class SessionDTO:
    user_id: AuthUserID
    token: Optional[SessionToken]
    failed_attempts: FailedLoginAttempts
    blocked_until: Optional[datetime]
