from dataclasses import dataclass
from typing import Optional

from app.context.user.domain.value_objects import (
    Email,
    Password,
    UserDeletedAt,
    UserID,
)


@dataclass(frozen=True)
class UserDTO:
    user_id: UserID
    email: Email
    password: Password
    deleted_at: Optional[UserDeletedAt] = None

    @property
    def is_deleted(self) -> bool:
        """Check if the user is soft deleted"""
        return self.deleted_at is not None
