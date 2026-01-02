from dataclasses import dataclass

from app.context.user.domain.value_objects import (
    UserDeletedAt,
    UserEmail,
    UserID,
    UserName,
    UserPassword,
)


@dataclass(frozen=True)
class UserDTO:
    """Domain data transfer object for User aggregate"""

    user_id: UserID
    email: UserEmail
    password: UserPassword
    username: UserName | None = None
    deleted_at: UserDeletedAt | None = None

    @property
    def is_deleted(self) -> bool:
        """Check if the user is soft deleted"""
        return self.deleted_at is not None
