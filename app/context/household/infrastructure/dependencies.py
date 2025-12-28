from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.household.application.contracts import (
    AcceptInviteHandlerContract,
    CreateHouseholdHandlerContract,
    DeclineInviteHandlerContract,
    InviteUserHandlerContract,
    ListHouseholdInvitesHandlerContract,
    ListUserPendingInvitesHandlerContract,
    RemoveMemberHandlerContract,
)
from app.context.household.application.handlers import (
    AcceptInviteHandler,
    CreateHouseholdHandler,
    DeclineInviteHandler,
    InviteUserHandler,
    ListHouseholdInvitesHandler,
    ListUserPendingInvitesHandler,
    RemoveMemberHandler,
)
from app.context.household.domain.contracts import (
    AcceptInviteServiceContract,
    CreateHouseholdServiceContract,
    DeclineInviteServiceContract,
    HouseholdRepositoryContract,
    InviteUserServiceContract,
    RemoveMemberServiceContract,
)
from app.context.household.domain.services import (
    AcceptInviteService,
    CreateHouseholdService,
    DeclineInviteService,
    InviteUserService,
    RemoveMemberService,
)
from app.context.household.infrastructure.repositories import HouseholdRepository
from app.shared.infrastructure.database import get_db


# Repository dependencies
def get_household_repository(
    db: AsyncSession = Depends(get_db),
) -> HouseholdRepositoryContract:
    return HouseholdRepository(db)


# Service dependencies
def get_create_household_service(
    household_repository: HouseholdRepositoryContract = Depends(get_household_repository),
) -> CreateHouseholdServiceContract:
    return CreateHouseholdService(household_repository)


def get_invite_user_service(
    household_repository: HouseholdRepositoryContract = Depends(get_household_repository),
) -> InviteUserServiceContract:
    return InviteUserService(household_repository)


def get_accept_invite_service(
    household_repository: HouseholdRepositoryContract = Depends(get_household_repository),
) -> AcceptInviteServiceContract:
    return AcceptInviteService(household_repository)


def get_decline_invite_service(
    household_repository: HouseholdRepositoryContract = Depends(get_household_repository),
) -> DeclineInviteServiceContract:
    return DeclineInviteService(household_repository)


def get_remove_member_service(
    household_repository: HouseholdRepositoryContract = Depends(get_household_repository),
) -> RemoveMemberServiceContract:
    return RemoveMemberService(household_repository)


# Handler dependencies (Commands)
def get_create_household_handler(
    service: CreateHouseholdServiceContract = Depends(get_create_household_service),
) -> CreateHouseholdHandlerContract:
    return CreateHouseholdHandler(service)


def get_invite_user_handler(
    service: InviteUserServiceContract = Depends(get_invite_user_service),
) -> InviteUserHandlerContract:
    return InviteUserHandler(service)


def get_accept_invite_handler(
    service: AcceptInviteServiceContract = Depends(get_accept_invite_service),
) -> AcceptInviteHandlerContract:
    return AcceptInviteHandler(service)


def get_decline_invite_handler(
    service: DeclineInviteServiceContract = Depends(get_decline_invite_service),
) -> DeclineInviteHandlerContract:
    return DeclineInviteHandler(service)


def get_remove_member_handler(
    service: RemoveMemberServiceContract = Depends(get_remove_member_service),
) -> RemoveMemberHandlerContract:
    return RemoveMemberHandler(service)


# Handler dependencies (Queries)
def get_list_household_invites_handler(
    repository: HouseholdRepositoryContract = Depends(get_household_repository),
) -> ListHouseholdInvitesHandlerContract:
    return ListHouseholdInvitesHandler(repository)


def get_list_user_pending_invites_handler(
    repository: HouseholdRepositoryContract = Depends(get_household_repository),
) -> ListUserPendingInvitesHandlerContract:
    return ListUserPendingInvitesHandler(repository)
