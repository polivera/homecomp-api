from dataclasses import dataclass


@dataclass(frozen=True)
class FindEntryByIdQuery:
    """Query for finding an entry by ID"""

    entry_id: int
    user_id: int
