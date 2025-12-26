from abc import ABC, abstractmethod
from typing import Optional

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects.account_id import AccountID
from app.context.user_account.domain.value_objects.account_name import AccountName


class UserAccountRepositoryContract(ABC):
    """Contract for user account repository operations"""

    @abstractmethod
    async def save_account(self, account: UserAccountDTO) -> UserAccountDTO:
        """
        Create a new user account

        Args:
            account: The account DTO to save

        Returns:
            UserAccountDTO of the created account

        Raises:
            Exception if account with same user_id and name already exists
        """
        pass

    @abstractmethod
    async def find_account(
        self,
        account_id: Optional[AccountID] = None,
        user_id: Optional[UserID] = None,
        name: Optional[AccountName] = None,
    ) -> Optional[UserAccountDTO]:
        """
        Find an account by ID or by user_id and name

        Args:
            account_id: Account ID to search for
            user_id: User ID to search for (combined with name)
            name: Account name to search for (combined with user_id)

        Returns:
            UserAccountDTO if found, None otherwise
        """
        pass

    @abstractmethod
    async def find_accounts_by_user(self, user_id: UserID) -> list[UserAccountDTO]:
        """
        Find all non-deleted accounts for a user

        Args:
            user_id: User ID to search for

        Returns:
            List of UserAccountDTO objects
        """
        pass

    @abstractmethod
    async def update_account(self, account: UserAccountDTO) -> UserAccountDTO:
        """
        Update an existing account

        Args:
            account: The account DTO with updated values

        Returns:
            Updated UserAccountDTO

        Raises:
            ValueError: If account not found or already deleted
        """
        pass

    @abstractmethod
    async def delete_account(self, account_id: AccountID, user_id: UserID) -> bool:
        """
        Soft delete an account. Returns True if deleted, False if not found/unauthorized

        Args:
            account_id: Account ID to delete
            user_id: User ID (for authorization check)

        Returns:
            True if successfully deleted, False if not found or unauthorized
        """
        pass
