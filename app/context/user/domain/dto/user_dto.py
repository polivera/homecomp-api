from dataclasses import dataclass
from app.shared.domain.valueobject import Email


@dataclass(frozen=True)
class UserDTO:
    email: Email
