from dataclasses import dataclass

from app.shared.domain.value_objects.shared_deleted_at import SharedDeletedAt


@dataclass(frozen=True)
class HouseholdDeletedAt(SharedDeletedAt):
    """Household context-specific deleted_at value object"""

    pass
