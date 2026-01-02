from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteEntryCommand:
    """Command for deleting an entry"""

    entry_id: int
    user_id: int
