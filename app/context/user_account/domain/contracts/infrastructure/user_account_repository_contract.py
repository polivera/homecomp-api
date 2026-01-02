from abc import ABC, abstractmethod

from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects import UserAccountUserID
from app.context.user_account.domain.value_objects.account_id import UserAccountID
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
            UserAccountMapperError if cannot map model to dto
            UserAccountNameAlreadyExistError if account name already exist
        """
        pass

    @abstractmethod
    async def find_account(
        self,
        account_id: UserAccountID | None = None,
        user_id: UserAccountUserID | None = None,
        name: AccountName | None = None,
    ) -> UserAccountDTO | None:
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
    async def find_user_accounts(
        self,
        user_id: UserAccountUserID,
        account_id: UserAccountID | None = None,
        name: AccountName | None = None,
        only_active: bool | None = True,
    ) -> list[UserAccountDTO] | None:
        """
        Find user account always filtering by user_id (for user-scoped queries)

        Args:
            user_id: User ID to filter accounts for
            account_id: Optional account ID to find specific account
            name: Optional account name for partial match search
            only_active: Whether to exclude soft-deleted accounts (default: True)

        Returns:
            UserAccountDTO if found, None otherwise
        """
        pass

    @abstractmethod
    async def find_user_account_by_id(
        self,
        user_id: UserAccountUserID,
        account_id: UserAccountID,
        only_active: bool | None = True,
    ) -> UserAccountDTO | None:
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
    async def delete_account(self, account_id: UserAccountID, user_id: UserAccountUserID) -> bool:
        """
        Soft delete an account. Returns True if deleted, False if not found/unauthorized

        Args:
            account_id: Account ID to delete
            user_id: User ID (for authorization check)

        Returns:
            True if successfully deleted, False if not found or unauthorized
        """
        pass
