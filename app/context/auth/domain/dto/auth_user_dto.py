from dataclasses import dataclass

from app.context.auth.domain.value_objects import AuthEmail, AuthPassword, AuthUserID


@dataclass(frozen=True)
class AuthUserDTO:
    user_id: AuthUserID
    email: AuthEmail
    password: AuthPassword
