from sqlalchemy.ext.asyncio import AsyncSession

from app.context.household.application.contracts import (
    AcceptInviteHandlerContract,
    CreateHouseholdHandlerContract,
    DeclineInviteHandlerContract,
    DeleteHouseholdHandlerContract,
    GetHouseholdHandlerContract,
    InviteUserHandlerContract,
    ListHouseholdInvitesHandlerContract,
    ListUserHouseholdsHandlerContract,
    ListUserPendingInvitesHandlerContract,
    RemoveMemberHandlerContract,
    UpdateHouseholdHandlerContract,
)
from app.shared.domain.contracts.logger import LoggerContract
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

        return login_handler_factory(self.db, self.logger)

    # =========================================================================
    # User Account Context
    # =========================================================================

    def get_create_account_handler(self):
        """Get create account handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            create_account_handler_factory,
        )

        return create_account_handler_factory(self.db, self.logger)

    def get_update_account_handler(self):
        """Get update account handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            update_account_handler_factory,
        )

        return update_account_handler_factory(self.db, self.logger)

    def get_delete_account_handler(self):
        """Get delete account handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            delete_account_handler_factory,
        )

        return delete_account_handler_factory(self.db, self.logger)

    def get_find_account_by_id_handler(self):
        """Get find account by id handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            find_account_by_id_handler_factory,
        )

        return find_account_by_id_handler_factory(self.db, self.logger)

    def get_find_accounts_by_user_handler(self):
        """Get find accounts by user handler with all dependencies"""
        from app.context.user_account.infrastructure.dependencies import (
            find_accounts_by_user_handler_factory,
        )

        return find_accounts_by_user_handler_factory(self.db, self.logger)

    # =========================================================================
    # Credit Card Context
    # =========================================================================

    def get_create_credit_card_handler(self):
        """Get create credit card handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            create_credit_card_handler_factory,
        )

        return create_credit_card_handler_factory(self.db, self.logger)

    def get_update_credit_card_handler(self):
        """Get update credit card handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            update_credit_card_handler_factory,
        )

        return update_credit_card_handler_factory(self.db, self.logger)

    def get_delete_credit_card_handler(self):
        """Get delete credit card handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            delete_credit_card_handler_factory,
        )

        return delete_credit_card_handler_factory(self.db, self.logger)

    def get_find_credit_card_by_id_handler(self):
        """Get find credit card by id handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            find_credit_card_by_id_handler_factory,
        )

        return find_credit_card_by_id_handler_factory(self.db, self.logger)

    def get_find_credit_cards_by_user_handler(self):
        """Get find credit cards by user handler with all dependencies"""
        from app.context.credit_card.infrastructure.dependencies import (
            find_credit_cards_by_user_handler_factory,
        )

        return find_credit_cards_by_user_handler_factory(self.db, self.logger)

    # =========================================================================
    # Entry Context
    # =========================================================================

    def get_create_entry_handler(self):
        """Get create entry handler with all dependencies"""
        from app.context.entry.infrastructure.dependencies import create_entry_handler_factory

        return create_entry_handler_factory(self.db, self.logger)

    def get_update_entry_handler(self):
        """Get update entry handler with all dependencies"""
        from app.context.entry.infrastructure.dependencies import update_entry_handler_factory

        return update_entry_handler_factory(self.db, self.logger)

    def get_delete_entry_handler(self):
        """Get delete entry handler with all dependencies"""
        from app.context.entry.infrastructure.dependencies import delete_entry_handler_factory

        return delete_entry_handler_factory(self.db, self.logger)

    def get_find_entry_by_id_handler(self):
        """Get find entry by id handler with all dependencies"""
        from app.context.entry.infrastructure.dependencies import find_entry_by_id_handler_factory

        return find_entry_by_id_handler_factory(self.db, self.logger)

    def get_find_entries_by_account_month_handler(self):
        """Get find entries by account and month handler with all dependencies"""
        from app.context.entry.infrastructure.dependencies import (
            find_entries_by_account_month_handler_factory,
        )

        return find_entries_by_account_month_handler_factory(self.db, self.logger)

    # =========================================================================
    # Household Context
    # =========================================================================
    def get_accept_invite_handler(self) -> AcceptInviteHandlerContract:
        """Get accept invite handler with all dependencies"""

        from app.context.household.infrastructure.dependencies import accept_invite_handler_factory

        return accept_invite_handler_factory(self.db, self.logger)

    def get_create_household_handler(self) -> CreateHouseholdHandlerContract:
        """Get create household handler"""
        from app.context.household.infrastructure.dependencies import create_household_handler_factory

        return create_household_handler_factory(self.db, self.logger)

    def get_decline_invite_handler(self) -> DeclineInviteHandlerContract:
        """Get decline invite household handler"""
        from app.context.household.infrastructure.dependencies import decline_invite_hanlder_factory

        return decline_invite_hanlder_factory(self.db, self.logger)

    def get_delete_household_handler(self) -> DeleteHouseholdHandlerContract:
        """Get delete household handler with all dependencies"""
        from app.context.household.infrastructure.dependencies import delete_household_hanlder_factory

        return delete_household_hanlder_factory(self.db, self.logger)

    def get_household_handler(self) -> GetHouseholdHandlerContract:
        """Get household handler iwth all dependencies"""
        from app.context.household.infrastructure.dependencies import get_household_handler_factory

        return get_household_handler_factory(self.db, self.logger)

    def get_invite_user_handler(self) -> InviteUserHandlerContract:
        """Get invite user handler with all dependencies"""
        from app.context.household.infrastructure.dependencies import invite_user_handler_factory

        return invite_user_handler_factory(self.db, self.logger)

    def get_remove_member_handler(self) -> RemoveMemberHandlerContract:
        """Get remove member handler with all dependencies"""
        from app.context.household.infrastructure.dependencies import remove_member_handler_factory

        return remove_member_handler_factory(self.db, self.logger)

    def get_update_household_handler(self) -> UpdateHouseholdHandlerContract:
        """Get update household handler with all dependencies"""
        from app.context.household.infrastructure.dependencies import update_household_handler_factory

        return update_household_handler_factory(self.db, self.logger)

    def get_list_household_invites_handler(self) -> ListHouseholdInvitesHandlerContract:
        """Get list household invites handler with all dependencies"""
        from app.context.household.infrastructure.dependencies import list_household_invites_handler_factory

        return list_household_invites_handler_factory(self.db, self.logger)

    def get_list_user_households_handler(self) -> ListUserHouseholdsHandlerContract:
        """Get list user households handler with all dependencies"""
        from app.context.household.infrastructure.dependencies import list_user_households_handler_factory

        return list_user_households_handler_factory(self.db, self.logger)

    def get_list_user_pending_invites_handler(self) -> ListUserPendingInvitesHandlerContract:
        """Get list user pending invites handler with all dependencies"""
        from app.context.household.infrastructure.dependencies import list_user_pending_invites_handler_factory

        return list_user_pending_invites_handler_factory(self.db, self.logger)

    # =========================================================================
    # Reminder Context
    # =========================================================================

    def get_create_reminder_handler(self):
        """Get create reminder handler with all dependencies"""
        from app.context.reminder.infrastructure.dependencies import get_create_reminder_handler

        return get_create_reminder_handler(self.db, self.logger)

    def get_update_reminder_handler(self):
        """Get update reminder handler with all dependencies"""
        from app.context.reminder.infrastructure.dependencies import get_update_reminder_handler

        return get_update_reminder_handler(self.db, self.logger)

    def get_delete_reminder_handler(self):
        """Get delete reminder handler with all dependencies"""
        from app.context.reminder.infrastructure.dependencies import get_delete_reminder_handler

        return get_delete_reminder_handler(self.db, self.logger)

    def get_find_reminder_handler(self):
        """Get find reminder handler with all dependencies"""
        from app.context.reminder.infrastructure.dependencies import get_find_reminder_handler

        return get_find_reminder_handler(self.db, self.logger)

    def get_list_reminders_handler(self):
        """Get list reminders handler with all dependencies"""
        from app.context.reminder.infrastructure.dependencies import get_list_reminders_handler

        return get_list_reminders_handler(self.db, self.logger)

    def get_list_occurrences_handler(self):
        """Get list occurrences handler with all dependencies"""
        from app.context.reminder.infrastructure.dependencies import get_list_occurrences_handler

        return get_list_occurrences_handler(self.db, self.logger)
