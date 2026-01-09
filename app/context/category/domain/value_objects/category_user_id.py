from dataclasses import dataclass

from app.shared.domain.value_objects import SharedUserID


@dataclass(frozen=True)
class CategoryUserID(SharedUserID):
    """Context-specific user ID for category context"""

    pass
