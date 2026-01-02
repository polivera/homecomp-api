from dataclasses import dataclass

from app.shared.domain.value_objects.shared_category_id import SharedCategoryID


@dataclass(frozen=True)
class EntryCategoryID(SharedCategoryID):
    """Entry context-specific wrapper for category identifier"""

    pass
