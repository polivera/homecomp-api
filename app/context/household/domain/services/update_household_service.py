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
from app.shared.domain.contracts import LoggerContract


class UpdateHouseholdService(UpdateHouseholdServiceContract):
    """Service for updating households"""

    def __init__(self, repository: HouseholdRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def update_household(
        self,
        household_id: HouseholdID,
        user_id: HouseholdUserID,
        name: HouseholdName,
    ) -> HouseholdDTO:
        """Update household name (owner only)"""

        self._logger.debug(
            "Updating household", household_id=household_id.value, user_id=user_id.value, name=name.value
        )

        # 1. Find existing household
        existing = await self._repository.find_household_by_id(household_id)

        if not existing:
            self._logger.debug("Household not found", household_id=household_id.value)
            raise HouseholdNotFoundError(f"Household with ID {household_id.value} not found")

        # 2. Verify user is owner
        if existing.owner_user_id.value != user_id.value:
            self._logger.warning(
                "Non-owner attempted to update household",
                household_id=household_id.value,
                user_id=user_id.value,
            )
            raise OnlyOwnerCanUpdateError("Only the household owner can update the household")

        # 3. Check duplicate name (if name changed)
        if existing.name.value != name.value:
            duplicate = await self._repository.find_household_by_name(name, user_id)
            if duplicate and duplicate.household_id and duplicate.household_id.value != household_id.value:
                self._logger.debug("Duplicate household name found", user_id=user_id.value, name=name.value)
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
