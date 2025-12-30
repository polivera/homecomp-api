from abc import ABC, abstractmethod

from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.value_objects import HouseholdID, HouseholdName, HouseholdUserID


class UpdateHouseholdServiceContract(ABC):
    """Contract for update household service"""

    @abstractmethod
    async def update_household(
        self,
        household_id: HouseholdID,
        user_id: HouseholdUserID,
        name: HouseholdName,
    ) -> HouseholdDTO:
        """Update household name (owner only)"""
        pass
