from dataclasses import dataclass

from app.shared.domain.value_objects import SharedDeletedAt


@dataclass(frozen=True)
class CategoryDeletedAt(SharedDeletedAt):
    """Context-specific deleted_at timestamp for category context"""

    pass
