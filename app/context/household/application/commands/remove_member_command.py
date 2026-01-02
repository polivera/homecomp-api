from dataclasses import dataclass


@dataclass(frozen=True)
class RemoveMemberCommand:
    """Command to remove a member from a household"""

    remover_user_id: int
    household_id: int
    member_user_id: int
