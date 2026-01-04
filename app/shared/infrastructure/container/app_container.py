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

    # =========================================================================
    # User Account Context
    # =========================================================================

    def get_create_account_handler(self):
        """Get create account handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            create_account_handler_factory,
        )

        return create_account_handler_factory(self._db, self._logger)

    def get_update_account_handler(self):
        """Get update account handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            update_account_handler_factory,
        )

        return update_account_handler_factory(self._db, self._logger)

    def get_delete_account_handler(self):
        """Get delete account handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            delete_account_handler_factory,
        )

        return delete_account_handler_factory(self._db, self._logger)

    def get_find_account_by_id_handler(self):
        """Get find account by id handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            find_account_by_id_handler_factory,
        )

        return find_account_by_id_handler_factory(self._db, self._logger)

    def get_find_accounts_by_user_handler(self):
        """Get find accounts by user handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            find_accounts_by_user_handler_factory,
        )

        return find_accounts_by_user_handler_factory(self._db, self._logger)

    # =========================================================================
    # Credit Card Context
    # =========================================================================

    def get_create_credit_card_handler(self):
        """Get create credit card handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            create_credit_card_handler_factory,
        )

        return create_credit_card_handler_factory(self._db, self._logger)

    def get_update_credit_card_handler(self):
        """Get update credit card handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            update_credit_card_handler_factory,
        )

        return update_credit_card_handler_factory(self._db, self._logger)

    def get_delete_credit_card_handler(self):
        """Get delete credit card handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            delete_credit_card_handler_factory,
        )

        return delete_credit_card_handler_factory(self._db, self._logger)

    def get_find_credit_card_by_id_handler(self):
        """Get find credit card by id handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            find_credit_card_by_id_handler_factory,
        )

        return find_credit_card_by_id_handler_factory(self._db, self._logger)

    def get_find_credit_cards_by_user_handler(self):
        """Get find credit cards by user handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            find_credit_cards_by_user_handler_factory,
        )

        return find_credit_cards_by_user_handler_factory(self._db, self._logger)
