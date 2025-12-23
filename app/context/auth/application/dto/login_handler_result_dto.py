from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class LoginHandlerResultStatus(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid"
    ACCOUNT_BLOCKED = "blocked"
    UNEXPECTED_ERROR = "unexpected_error"


@dataclass(frozen=True)
class LoginHandlerResultDTO:
    status: LoginHandlerResultStatus
    token: Optional[str] = None
    user_id: Optional[int] = None
    error_msg: Optional[str] = None
    retry_after: Optional[datetime] = None
