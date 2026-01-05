from typing import Annotated

from fastapi import APIRouter, Depends

from app.context.household.application.queries import ListUserPendingInvitesQuery
from app.context.household.interface.schemas import HouseholdMemberResponse
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.get("/invites/pending", status_code=200)
async def list_user_pending_invites(
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[HouseholdMemberResponse]:
    """List all pending invitations for the authenticated user"""
    logger = app_container.logger
    handler = app_container.get_list_user_pending_invites_handler()

    logger.info("List user pending invites request", user_id=user_id)

    query = ListUserPendingInvitesQuery(user_id=user_id)

    members = await handler.handle(query)

    logger.info("User pending invites retrieved successfully", user_id=user_id, count=len(members))
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
