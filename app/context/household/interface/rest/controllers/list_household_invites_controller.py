from typing import Annotated

from fastapi import APIRouter, Depends

from app.context.household.application.queries import ListHouseholdInvitesQuery
from app.context.household.interface.schemas import HouseholdMemberResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.get("/{household_id}/invites", status_code=200)
async def list_household_invites(
    household_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[HouseholdMemberResponse]:
    """List pending invitations for a household"""
    logger = app_container.logger
    handler = app_container.get_list_household_invites_handler()

    logger.info("List household invites request", household_id=household_id, user_id=user_id)

    query = ListHouseholdInvitesQuery(household_id=household_id, user_id=user_id)

    members = await handler.handle(query)

    logger.info("Household invites retrieved successfully", household_id=household_id, count=len(members))
    return [
        HouseholdMemberResponse(
            member_id=member.member_id,
            household_id=member.household_id,
            user_id=member.user_id,
            role=member.role,
            joined_at=member.joined_at,
            invited_by_user_id=member.invited_by_user_id,
            invited_at=member.invited_at,
            household_name=member.household_name,
            inviter=member.inviter,
        )
        for member in members
    ]
