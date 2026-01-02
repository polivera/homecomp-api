from app.context.household.application.contracts import ListUserHouseholdsHandlerContract
from app.context.household.application.dto import (
    HouseholdSummary,
    ListUserHouseholdsErrorCode,
    ListUserHouseholdsResult,
)
from app.context.household.application.queries import ListUserHouseholdsQuery
from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.value_objects import HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class ListUserHouseholdsHandler(ListUserHouseholdsHandlerContract):
    """Handler for list user households query"""

    def __init__(self, repository: HouseholdRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def handle(self, query: ListUserHouseholdsQuery) -> ListUserHouseholdsResult:
        """Execute the list user households query"""

        self._logger.debug("Handling list user households query", user_id=query.user_id)

        try:
            # Convert primitive to value object
            user_id = HouseholdUserID(query.user_id)

            # Get all households for user
            households = await self._repository.list_user_households(user_id)

            # Convert DTOs to summary primitives
            summaries = [
                HouseholdSummary(
                    household_id=h.household_id.value if h.household_id else 0,
                    household_name=h.name.value,
                    owner_user_id=h.owner_user_id.value,
                    created_at=h.created_at.isoformat() if h.created_at else "",
                )
                for h in households
            ]

            return ListUserHouseholdsResult(households=summaries)

        except Exception as e:
            self._logger.error("Unexpected error listing user households", user_id=query.user_id, error=str(e))
            return ListUserHouseholdsResult(
                error_code=ListUserHouseholdsErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
