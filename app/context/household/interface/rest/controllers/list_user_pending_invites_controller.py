from typing import Annotated

from fastapi import APIRouter, Depends

from app.context.household.application.contracts import (
    ListUserPendingInvitesHandlerContract,
)
from app.context.household.application.queries import ListUserPendingInvitesQuery
from app.context.household.infrastructure.dependencies import (
    get_list_user_pending_invites_handler,
)
from app.context.household.interface.schemas import HouseholdMemberResponse
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter()


@router.get("/invites/pending", status_code=200)
async def list_user_pending_invites(
    handler: Annotated[
        ListUserPendingInvitesHandlerContract, Depends(get_list_user_pending_invites_handler)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[HouseholdMemberResponse]:
    """List all pending invitations for the authenticated user"""

    query = ListUserPendingInvitesQuery(user_id=user_id)

    members = await handler.handle(query)

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
