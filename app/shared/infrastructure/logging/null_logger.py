from typing import Any

from app.shared.domain.contracts.logger import LoggerContract


class NullLogger(LoggerContract):
    """Null logger implementation that suppresses all log output.

    Useful for testing environments where log output is not desired.
    """

    def debug(self, message: str, **kwargs: Any) -> None:
        """No-op debug logging."""
        pass

    def info(self, message: str, **kwargs: Any) -> None:
        """No-op info logging."""
        pass

    def warning(self, message: str, **kwargs: Any) -> None:
        """No-op warning logging."""
        pass

    def error(self, message: str, **kwargs: Any) -> None:
        """No-op error logging."""
        pass

    def critical(self, message: str, **kwargs: Any) -> None:
        """No-op critical logging."""
        pass

    def bind(self, **kwargs: Any) -> LoggerContract:
        """Return the same null logger (binding has no effect)."""
        return self
