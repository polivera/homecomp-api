"""Domain exceptions for User context"""


class UserMapperError(Exception):
    """Raised when there's an error mapping between model and DTO"""

    pass


class UserEmailAlreadyExistError(Exception):
    """Raised when attempting to create a user with an email that already exists"""

    pass


class UserNotFoundError(Exception):
    """Raised when a requested user cannot be found"""

    pass


class InvalidUserPasswordError(Exception):
    """Raised when password validation fails"""

    pass


class InvalidEmailFormatError(Exception):
    """Raised when email format validation fails"""

    pass


class InvalidPasswordLengthError(Exception):
    """Raised when password length validation fails"""

    pass
