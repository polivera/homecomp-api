from dataclasses import dataclass


@dataclass(frozen=True)
class UserContextDTO:
    user_id: int
    email: str
    password: str
