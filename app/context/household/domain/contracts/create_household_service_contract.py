from abc import ABC, abstractmethod

from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.value_objects import HouseholdName, HouseholdUserID


class CreateHouseholdServiceContract(ABC):
    @abstractmethod
    async def create_household(self, name: HouseholdName, creator_user_id: HouseholdUserID) -> HouseholdDTO:
        """Create a new household with the creator as the first member"""
        pass
