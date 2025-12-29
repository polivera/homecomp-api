from dataclasses import dataclass

from app.shared.domain.value_objects.shared_password import SharedPassword


@dataclass(frozen=True)
class UserPassword(SharedPassword):
    """
    Context-specific Password value object for User context.
    Extends SharedPassword to maintain bounded context isolation.
    Password always represents a hashed value in the domain.
    """

    pass
