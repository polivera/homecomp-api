# Value Object Exceptions

class InvalidCardLimitTypeError(Exception):
    pass


class InvalidCardLimitValueError(Exception):
    pass


class InvalidCardLimitPrecisionError(Exception):
    pass


class InvalidCardLimitFormatError(Exception):
    pass


class InvalidCardUsedTypeError(Exception):
    pass


class InvalidCardUsedValueError(Exception):
    pass


class InvalidCardUsedPrecisionError(Exception):
    pass


class InvalidCardUsedFormatError(Exception):
    pass


class InvalidCreditCardNameTypeError(Exception):
    pass


class InvalidCreditCardNameLengthError(Exception):
    pass


class InvalidCreditCardIdTypeError(Exception):
    pass


class InvalidCreditCardIdValueError(Exception):
    pass


# Domain Service Exceptions

class CreditCardNotFoundError(Exception):
    pass


class CreditCardUnauthorizedAccessError(Exception):
    pass


class CreditCardNameAlreadyExistError(Exception):
    pass


class CreditCardUsedExceedsLimitError(Exception):
    pass


# Repository Exceptions

class CreditCardCreationError(Exception):
    pass


class CreditCardRepositoryInvalidParametersError(Exception):
    pass


class CreditCardUpdateWithoutIdError(Exception):
    pass


class CreditCardUpdateError(Exception):
    pass


class CreditCardMapperError(Exception):
    pass


class CreditCardDatabaseError(Exception):
    pass
