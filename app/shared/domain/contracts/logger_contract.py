from abc import ABC, abstractmethod
from typing import Any


class LoggerContract(ABC):
    """Contract for logging operations across the application."""

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message with optional structured data."""
        pass

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message with optional structured data."""
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message with optional structured data."""
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message with optional structured data."""
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message with optional structured data."""
        pass

    @abstractmethod
    def bind(self, **kwargs: Any) -> "LoggerContract":
        """Return a new logger with bound context variables."""
        pass
