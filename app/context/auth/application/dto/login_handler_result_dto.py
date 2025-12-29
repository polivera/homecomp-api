from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LoginHandlerResultStatus(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid"
    ACCOUNT_BLOCKED = "blocked"
    UNEXPECTED_ERROR = "unexpected_error"


@dataclass(frozen=True)
class LoginHandlerResultDTO:
    status: LoginHandlerResultStatus
    token: str | None = None
    user_id: int | None = None
    error_msg: str | None = None
    retry_after: datetime | None = None
