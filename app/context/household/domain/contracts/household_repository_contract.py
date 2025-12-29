from abc import ABC, abstractmethod

from app.context.household.domain.dto import HouseholdDTO, HouseholdMemberDTO
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)


class HouseholdRepositoryContract(ABC):
    @abstractmethod
    async def create_household(
        self, household_dto: HouseholdDTO, creator_user_id: HouseholdUserID
    ) -> HouseholdDTO:
        """Create a new household and add the creator as first member"""
        pass

    @abstractmethod
    async def find_household_by_name(
        self, name: HouseholdName, user_id: HouseholdUserID
    ) -> HouseholdDTO | None:
        """Find a household by name for a specific user"""
        pass

    @abstractmethod
    async def find_household_by_id(
        self, household_id: HouseholdID
    ) -> HouseholdDTO | None:
        """Find a household by ID"""
        pass

    # Member management methods
    @abstractmethod
    async def create_member(self, member: HouseholdMemberDTO) -> HouseholdMemberDTO:
        """Create a new household member (for invites or direct adds)"""
        pass

    @abstractmethod
    async def find_member(
        self, household_id: HouseholdID, user_id: HouseholdUserID
    ) -> HouseholdMemberDTO | None:
        """Find the most recent member record for user in household"""
        pass

    @abstractmethod
    async def accept_invite(
        self, household_id: HouseholdID, user_id: HouseholdUserID
    ) -> HouseholdMemberDTO:
        """Accept invite by setting joined_at to current timestamp"""
        pass

    @abstractmethod
    async def revoke_or_remove(
        self, household_id: HouseholdID, user_id: HouseholdUserID
    ) -> None:
        """Revoke invite or remove member by setting left_at to current timestamp"""
        pass

    @abstractmethod
    async def list_user_households(
        self, user_id: HouseholdUserID
    ) -> list[HouseholdDTO]:
        """List all households user owns or is an active participant in"""
        pass

    @abstractmethod
    async def list_user_pending_invites(
        self, user_id: HouseholdUserID
    ) -> list[HouseholdDTO]:
        """List all households user has been invited to but not yet accepted"""
        pass

    @abstractmethod
    async def list_household_pending_invites(
        self, household_id: HouseholdID, owner_id: HouseholdUserID
    ) -> list[HouseholdMemberDTO]:
        """List all pending invites for a household"""
        pass

    @abstractmethod
    async def list_user_pending_household_invites(
        self, user_id: HouseholdUserID
    ) -> list[HouseholdMemberDTO]:
        """List user pending invitation to households"""
        pass

    @abstractmethod
    async def user_has_access(
        self, user_id: HouseholdUserID, household_id: HouseholdID
    ) -> bool:
        """Check if user owns or is an active member of household"""
        pass
