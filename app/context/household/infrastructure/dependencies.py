from typing import Annotated

from fastapi import Depends
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
from app.context.household.application.handlers import (
    AcceptInviteHandler,
    CreateHouseholdHandler,
    DeclineInviteHandler,
    DeleteHouseholdHandler,
    GetHouseholdHandler,
    InviteUserHandler,
    ListHouseholdInvitesHandler,
    ListUserHouseholdsHandler,
    ListUserPendingInvitesHandler,
    RemoveMemberHandler,
    UpdateHouseholdHandler,
)
from app.context.household.domain.contracts import (
    AcceptInviteServiceContract,
    CreateHouseholdServiceContract,
    DeclineInviteServiceContract,
    HouseholdRepositoryContract,
    InviteUserServiceContract,
    RemoveMemberServiceContract,
    RevokeInviteServiceContract,
    UpdateHouseholdServiceContract,
)
from app.context.household.domain.services import (
    AcceptInviteService,
    CreateHouseholdService,
    DeclineInviteService,
    InviteUserService,
    RemoveMemberService,
    RevokeInviteService,
    UpdateHouseholdService,
)
from app.context.household.infrastructure.repositories import HouseholdRepository
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.database import get_db
from app.shared.infrastructure.dependencies import get_logger


# Repository dependencies
def get_household_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HouseholdRepositoryContract:
    return HouseholdRepository(db)


# Service dependencies
def get_create_household_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> CreateHouseholdServiceContract:
    return CreateHouseholdService(household_repository, logger)


def get_invite_user_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> InviteUserServiceContract:
    return InviteUserService(household_repository, logger)


def get_accept_invite_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> AcceptInviteServiceContract:
    return AcceptInviteService(household_repository, logger)


def get_decline_invite_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> DeclineInviteServiceContract:
    return DeclineInviteService(household_repository, logger)


def get_remove_member_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> RemoveMemberServiceContract:
    return RemoveMemberService(household_repository, logger)


def get_update_household_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> UpdateHouseholdServiceContract:
    return UpdateHouseholdService(household_repository, logger)


def get_revoke_invite_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> RevokeInviteServiceContract:
    return RevokeInviteService(household_repository, logger)


# Handler dependencies (Commands)
def get_create_household_handler(
    service: Annotated[CreateHouseholdServiceContract, Depends(get_create_household_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> CreateHouseholdHandlerContract:
    return CreateHouseholdHandler(service, logger)


def get_invite_user_handler(
    service: Annotated[InviteUserServiceContract, Depends(get_invite_user_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> InviteUserHandlerContract:
    return InviteUserHandler(service, logger)


def get_accept_invite_handler(
    service: Annotated[AcceptInviteServiceContract, Depends(get_accept_invite_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> AcceptInviteHandlerContract:
    return AcceptInviteHandler(service, logger)


def get_decline_invite_handler(
    service: Annotated[DeclineInviteServiceContract, Depends(get_decline_invite_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> DeclineInviteHandlerContract:
    return DeclineInviteHandler(service, logger)


def get_remove_member_handler(
    service: Annotated[RemoveMemberServiceContract, Depends(get_remove_member_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> RemoveMemberHandlerContract:
    return RemoveMemberHandler(service, logger)


def get_update_household_handler(
    service: Annotated[UpdateHouseholdServiceContract, Depends(get_update_household_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> UpdateHouseholdHandlerContract:
    return UpdateHouseholdHandler(service, logger)


def get_delete_household_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> DeleteHouseholdHandlerContract:
    return DeleteHouseholdHandler(repository, logger)


# Handler dependencies (Queries)
def get_list_household_invites_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> ListHouseholdInvitesHandlerContract:
    return ListHouseholdInvitesHandler(repository, logger)


def get_list_user_pending_invites_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> ListUserPendingInvitesHandlerContract:
    return ListUserPendingInvitesHandler(repository, logger)


def get_get_household_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> GetHouseholdHandlerContract:
    return GetHouseholdHandler(repository, logger)


def get_list_user_households_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> ListUserHouseholdsHandlerContract:
    return ListUserHouseholdsHandler(repository, logger)
