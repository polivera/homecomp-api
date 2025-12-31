from dataclasses import dataclass

from app.shared.domain.value_objects.shared_account_id import SharedAccountID


@dataclass(frozen=True)
class EntryAccountID(SharedAccountID):
    """Entry context-specific wrapper for account identifier"""

    pass
