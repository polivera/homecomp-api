from abc import ABC, abstractmethod
from typing import Optional

from app.context.user.domain.dto import UserDTO
from app.context.user.domain.value_objects import UserEmail, UserID


class UserRepositoryContract(ABC):
    """Contract for User repository operations"""

    @abstractmethod
    async def find_user(
        self, user_id: Optional[UserID] = None, email: Optional[UserEmail] = None
    ) -> Optional[UserDTO]:
        """
        Find a user by ID or email.

        Args:
            user_id: Optional user ID to search by
            email: Optional email to search by

        Returns:
            UserDTO if found, None otherwise
        """
        pass
