"""Domain exceptions for reminder context"""


class ReminderNotFoundError(Exception):
    """Raised when a reminder is not found"""

    pass


class ReminderNotBelongsToUserError(Exception):
    """Raised when a reminder does not belong to the user"""

    pass


class ReminderMapperError(Exception):
    """Raised when mapping between model and DTO fails"""

    pass


class ReminderOccurrenceNotFoundError(Exception):
    """Raised when a reminder occurrence is not found"""

    pass


class ReminderOccurrenceMapperError(Exception):
    """Raised when mapping between occurrence model and DTO fails"""

    pass


class InvalidReminderFrequencyError(Exception):
    """Raised when an invalid reminder frequency is provided"""

    pass


class InvalidReminderDateRangeError(Exception):
    """Raised when end_date is before start_date"""

    pass
