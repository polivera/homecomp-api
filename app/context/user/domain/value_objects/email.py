from dataclasses import dataclass

from app.shared.domain.value_objects.shared_email import SharedEmail


@dataclass(frozen=True)
class UserEmail(SharedEmail):
    """
    Context-specific Email value object for User context.
    Extends SharedEmail to maintain bounded context isolation.
    """

    pass
