from dataclasses import dataclass

from app.shared.domain.value_objects import SharedYear


@dataclass(frozen=True)
class EntryYear(SharedYear):
    pass
