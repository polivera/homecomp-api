from dataclasses import dataclass

from app.context.user.domain.value_objects import Email, Password, UserID


@dataclass(frozen=True)
class UserDTO:
    user_id: UserID
    email: Email
    password: Password
