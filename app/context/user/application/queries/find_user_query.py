from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FindUserQuery:
    id: Optional[int]
    email: Optional[str]
    password: Optional[str]
