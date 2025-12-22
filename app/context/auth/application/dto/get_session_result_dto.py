from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GetSessionResultDTO:
    user_id: int
    token: Optional[str]
    failed_attempts: int
    blocked_until: Optional[str]
