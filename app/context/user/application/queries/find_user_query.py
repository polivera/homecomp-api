from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FindUserQuery:
    user_id: Optional[int] = None
    email: Optional[str] = None
