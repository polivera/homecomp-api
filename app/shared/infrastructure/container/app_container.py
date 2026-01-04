from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger


class ApplicationContainer:
    _db: AsyncSession
    _logger: LoggerContract

    def __init__(self, db: AsyncSession):
        self._db = db
        self._logger = get_logger()

    @property
    def db(self) -> AsyncSession:
        """Get database session"""
        return self._db

    @property
    def logger(self) -> LoggerContract:
        """Get logger instance"""
        return self._logger

    # =========================================================================
    # Auth Context
    # =========================================================================

    def get_login_handler(self):
        """Get login handler with all dependencies"""
        from app.context.auth.infrastructure.dependencies import login_handler_factory

        return login_handler_factory(self._db, self._logger)
