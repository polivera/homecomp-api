from dataclasses import dataclass

@dataclass(frozen=True)
class UserContextDTO:
    id: int
    email: str
