class EntryMapperError(Exception):
    """Raised when entry mapper fails to convert between model and DTO"""

    pass


class EntryNotFoundError(Exception):
    """Raised when entry is not found"""

    pass


class EntryAccountNotBelongsToUserError(Exception):
    """Raised when account does not belong to the user"""

    pass


class EntryCategoryNotFoundError(Exception):
    """Raised when category is not found"""

    pass


class EntryCategoryNotBelongsToUserError(Exception):
    """Raised when category does not belong to the user"""

    pass


class EntryNotBelongsToUserError(Exception):
    """Raised when entry does not belong to the user"""

    pass
