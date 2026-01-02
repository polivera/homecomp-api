from app.context.household.domain.contracts import (
    CreateHouseholdServiceContract,
    HouseholdRepositoryContract,
)
from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.value_objects import HouseholdName, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class CreateHouseholdService(CreateHouseholdServiceContract):
    def __init__(self, household_repository: HouseholdRepositoryContract, logger: LoggerContract):
        self._household_repository = household_repository
        self._logger = logger

    async def create_household(self, name: HouseholdName, creator_user_id: HouseholdUserID) -> HouseholdDTO:
        """Create a new household with the creator as owner"""

        self._logger.debug("Creating household", user_id=creator_user_id.value, household_name=name.value)

        # Create new household DTO with owner
        household_dto = HouseholdDTO(
            household_id=None,
            owner_user_id=creator_user_id,
            name=name,
        )

        # Save to repository - will raise HouseholdNameAlreadyExistError if duplicate
        created_household = await self._household_repository.create_household(household_dto=household_dto)

        return created_household
