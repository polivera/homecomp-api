from dataclasses import dataclass


@dataclass(frozen=True)
class ListHouseholdInvitesQuery:
    """Query to list pending invites for a household"""

    household_id: int
    user_id: int
