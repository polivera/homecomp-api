from abc import ABC, abstractmethod
from typing import Optional

from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.value_objects import HouseholdID, HouseholdName, HouseholdUserID


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
    ) -> Optional[HouseholdDTO]:
        """Find a household by name for a specific user"""
        pass

    @abstractmethod
    async def find_household_by_id(self, household_id: HouseholdID) -> Optional[HouseholdDTO]:
        """Find a household by ID"""
        pass
