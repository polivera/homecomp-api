from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GetSessionQuery:
    user_id: Optional[int] = None
    token: Optional[str] = None
