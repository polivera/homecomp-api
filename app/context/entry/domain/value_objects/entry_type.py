from dataclasses import dataclass

from app.shared.domain.value_objects.shared_entry_type import SharedEntryType


@dataclass(frozen=True)
class EntryType(SharedEntryType):
    pass
