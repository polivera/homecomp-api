from app.context.household.application.contracts import GetHouseholdHandlerContract
from app.context.household.application.dto import GetHouseholdErrorCode, GetHouseholdResult
from app.context.household.application.queries import GetHouseholdQuery
from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class GetHouseholdHandler(GetHouseholdHandlerContract):
    """Handler for get household query"""

    def __init__(self, repository: HouseholdRepositoryContract):
        self._repository = repository

    async def handle(self, query: GetHouseholdQuery) -> GetHouseholdResult:
        """Execute the get household query"""
        try:
            # Convert primitives to value objects
            household_id = HouseholdID(query.household_id)
            user_id = HouseholdUserID(query.user_id)

            # Check if user has access (owner or active member)
            has_access = await self._repository.user_has_access(user_id, household_id)
            if not has_access:
                return GetHouseholdResult(
                    error_code=GetHouseholdErrorCode.UNAUTHORIZED_ACCESS,
                    error_message="You do not have access to this household",
                )

            # Find the household
            household = await self._repository.find_household_by_id(household_id)
            if not household:
                return GetHouseholdResult(
                    error_code=GetHouseholdErrorCode.NOT_FOUND,
                    error_message="Household not found",
                )

            # Return success with primitives
            return GetHouseholdResult(
                household_id=household.household_id.value if household.household_id else None,
                household_name=household.name.value,
                owner_user_id=household.owner_user_id.value,
                created_at=household.created_at.isoformat() if household.created_at else None,
            )

        except Exception:
            return GetHouseholdResult(
                error_code=GetHouseholdErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
