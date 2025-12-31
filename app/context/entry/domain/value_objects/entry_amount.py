from dataclasses import dataclass

from app.shared.domain.value_objects.shared_amount import SharedAmount


@dataclass(frozen=True)
class EntryAmount(SharedAmount):
    """Entry context-specific wrapper for monetary amounts"""

    pass
