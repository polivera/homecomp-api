from dataclasses import dataclass

from app.shared.domain.value_objects import SharedMonth


@dataclass(frozen=True)
class EntryMonth(SharedMonth):
    pass
