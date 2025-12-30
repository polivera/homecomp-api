from app.context.household.domain.contracts import (
    HouseholdRepositoryContract,
    UpdateHouseholdServiceContract,
)
from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.exceptions import (
    HouseholdNameAlreadyExistError,
    HouseholdNotFoundError,
    OnlyOwnerCanUpdateError,
)
from app.context.household.domain.value_objects import HouseholdID, HouseholdName, HouseholdUserID


class UpdateHouseholdService(UpdateHouseholdServiceContract):
    """Service for updating households"""

    def __init__(self, repository: HouseholdRepositoryContract):
        self._repository = repository

    async def update_household(
        self,
        household_id: HouseholdID,
        user_id: HouseholdUserID,
        name: HouseholdName,
    ) -> HouseholdDTO:
        """Update household name (owner only)"""

        # 1. Find existing household
        existing = await self._repository.find_household_by_id(household_id)

        if not existing:
            raise HouseholdNotFoundError(f"Household with ID {household_id.value} not found")

        # 2. Verify user is owner
        if existing.owner_user_id.value != user_id.value:
            raise OnlyOwnerCanUpdateError("Only the household owner can update the household")

        # 3. Check duplicate name (if name changed)
        if existing.name.value != name.value:
            duplicate = await self._repository.find_household_by_name(name, user_id)
            if duplicate and duplicate.household_id and duplicate.household_id.value != household_id.value:
                raise HouseholdNameAlreadyExistError(f"Household with name '{name.value}' already exists")

        # 4. Create updated DTO
        updated_dto = HouseholdDTO(
            household_id=household_id,
            owner_user_id=user_id,
            name=name,
            created_at=existing.created_at,
        )

        # 5. Persist and return
        return await self._repository.update_household(updated_dto)
