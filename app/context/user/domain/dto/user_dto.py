from dataclasses import dataclass

from app.context.user.domain.value_objects import Email


@dataclass(frozen=True)
class UserDTO:
    email: Email
