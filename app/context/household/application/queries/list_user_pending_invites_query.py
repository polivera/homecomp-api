from dataclasses import dataclass


@dataclass(frozen=True)
class ListUserPendingInvitesQuery:
    """Query to list all pending invites for a user"""

    user_id: int
