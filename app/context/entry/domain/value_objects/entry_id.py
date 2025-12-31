from dataclasses import dataclass

from app.shared.domain.value_objects.shared_entry_id import SharedEntryID


@dataclass(frozen=True)
class EntryID(SharedEntryID):
    """Entry context-specific wrapper for entry identifier"""

    pass
