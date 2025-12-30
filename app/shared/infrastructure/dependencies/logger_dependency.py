from os import getenv

from app.shared.domain.contracts.logger_contract import LoggerContract
from app.shared.infrastructure.logging import NullLogger, StructlogLogger


def get_logger() -> LoggerContract:
    """
    Factory function for dependency injection of the logger.

    Returns:
        LoggerContract: The configured logger implementation.
            - In test environment (APP_ENV=test): Returns NullLogger
            - Otherwise: Returns StructlogLogger
    """
    if getenv("APP_ENV") == "test":
        return NullLogger()

    return StructlogLogger()
