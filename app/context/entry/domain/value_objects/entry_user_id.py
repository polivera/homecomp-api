from dataclasses import dataclass

from app.shared.domain.value_objects.shared_user_id import SharedUserID


@dataclass(frozen=True)
class EntryUserID(SharedUserID):
    """Entry context-specific wrapper for user identifier"""

    pass
