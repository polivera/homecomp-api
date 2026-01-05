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
from app.context.household.domain.contracts import (
    AcceptInviteServiceContract,
    CreateHouseholdServiceContract,
    DeclineInviteServiceContract,
    HouseholdRepositoryContract,
    InviteUserServiceContract,
    RemoveMemberServiceContract,
    UpdateHouseholdServiceContract,
)
from app.shared.domain.contracts import LoggerContract

# ─────────────────────────────────────────────────────────────────
# COMMAND HANDLERS (Write operations)
# ─────────────────────────────────────────────────────────────────


def accept_invite_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> AcceptInviteHandlerContract:
    from app.context.household.application.handlers import AcceptInviteHandler

    household_repository = _get_household_repository(db)
    service = _get_accept_invite_service(household_repository, logger)
    return AcceptInviteHandler(service, logger)


def create_household_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> CreateHouseholdHandlerContract:
    from app.context.household.application.handlers import CreateHouseholdHandler

    household_repo = _get_household_repository(db)
    service = _get_create_household_service(household_repo, logger)
    return CreateHouseholdHandler(service, logger)


def decline_invite_hanlder_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> DeclineInviteHandlerContract:
    from app.context.household.application.handlers import DeclineInviteHandler

    household_repo = _get_household_repository(db)
    decline_invite_service = _get_decline_invite_service(household_repo, logger)
    return DeclineInviteHandler(decline_invite_service, logger)


def delete_household_hanlder_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> DeleteHouseholdHandlerContract:
    from app.context.household.application.handlers import DeleteHouseholdHandler

    repository = _get_household_repository(db)
    return DeleteHouseholdHandler(repository, logger)


def get_household_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> GetHouseholdHandlerContract:
    from app.context.household.application.handlers import GetHouseholdHandler

    repository = _get_household_repository(db)
    return GetHouseholdHandler(repository, logger)


def invite_user_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> InviteUserHandlerContract:
    from app.context.household.application.handlers import InviteUserHandler

    household_repo = _get_household_repository(db)
    service = _get_invite_user_service(household_repo, logger)
    return InviteUserHandler(service, logger)


def remove_member_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> RemoveMemberHandlerContract:
    from app.context.household.application.handlers import RemoveMemberHandler

    household_repo = _get_household_repository(db)
    service = _get_remove_member_service(household_repo, logger)
    return RemoveMemberHandler(service, logger)


def update_household_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> UpdateHouseholdHandlerContract:
    from app.context.household.application.handlers import UpdateHouseholdHandler

    household_repo = _get_household_repository(db)
    service = _get_update_household_service(household_repo, logger)
    return UpdateHouseholdHandler(service, logger)


# ─────────────────────────────────────────────────────────────────
# QUERY HANDLERS (Read operations)
# ─────────────────────────────────────────────────────────────────


def list_household_invites_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> ListHouseholdInvitesHandlerContract:
    from app.context.household.application.handlers import ListHouseholdInvitesHandler

    repository = _get_household_repository(db)
    return ListHouseholdInvitesHandler(repository, logger)


def list_user_households_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> ListUserHouseholdsHandlerContract:
    from app.context.household.application.handlers import ListUserHouseholdsHandler

    repository = _get_household_repository(db)
    return ListUserHouseholdsHandler(repository, logger)


def list_user_pending_invites_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> ListUserPendingInvitesHandlerContract:
    from app.context.household.application.handlers import ListUserPendingInvitesHandler

    repository = _get_household_repository(db)
    return ListUserPendingInvitesHandler(repository, logger)


# ─────────────────────────────────────────────────────────────────
# Private helper functions
# ─────────────────────────────────────────────────────────────────


def _get_accept_invite_service(
    household_repository: HouseholdRepositoryContract,
    logger: LoggerContract,
) -> AcceptInviteServiceContract:
    from app.context.household.domain.services import AcceptInviteService

    return AcceptInviteService(household_repository, logger)


def _get_household_repository(
    db: AsyncSession,
) -> HouseholdRepositoryContract:
    from app.context.household.infrastructure.repositories import HouseholdRepository

    return HouseholdRepository(db)


def _get_create_household_service(
    household_repository: HouseholdRepositoryContract,
    logger: LoggerContract,
) -> CreateHouseholdServiceContract:
    from app.context.household.domain.services import CreateHouseholdService

    return CreateHouseholdService(household_repository, logger)


def _get_decline_invite_service(
    household_repository: HouseholdRepositoryContract,
    logger: LoggerContract,
) -> DeclineInviteServiceContract:
    from app.context.household.domain.services import DeclineInviteService

    return DeclineInviteService(household_repository, logger)


def _get_invite_user_service(
    household_repository: HouseholdRepositoryContract,
    logger: LoggerContract,
) -> InviteUserServiceContract:
    from app.context.household.domain.services import InviteUserService

    return InviteUserService(household_repository, logger)


def _get_remove_member_service(
    household_repository: HouseholdRepositoryContract,
    logger: LoggerContract,
) -> RemoveMemberServiceContract:
    from app.context.household.domain.services import RemoveMemberService

    return RemoveMemberService(household_repository, logger)


def _get_update_household_service(
    household_repository: HouseholdRepositoryContract,
    logger: LoggerContract,
) -> UpdateHouseholdServiceContract:
    from app.context.household.domain.services import UpdateHouseholdService

    return UpdateHouseholdService(household_repository, logger)
