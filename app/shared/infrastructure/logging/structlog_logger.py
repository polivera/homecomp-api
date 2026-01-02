from typing import Any

import structlog

from app.shared.domain.contracts.logger_contract import LoggerContract


class StructlogLogger(LoggerContract):
    """Structlog implementation of the logger contract."""

    def __init__(self, logger: structlog.BoundLogger | None = None):
        """
        Initialize the structlog logger.

        Args:
            logger: Optional pre-configured structlog logger. If None, creates a new one.
        """
        self._logger = logger if logger is not None else structlog.get_logger()

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message with optional structured data."""
        self._logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message with optional structured data."""
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message with optional structured data."""
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message with optional structured data."""
        self._logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message with optional structured data."""
        self._logger.critical(message, **kwargs)

    def bind(self, **kwargs: Any) -> LoggerContract:
        """Return a new logger with bound context variables."""
        bound_logger = self._logger.bind(**kwargs)
        return StructlogLogger(logger=bound_logger)
