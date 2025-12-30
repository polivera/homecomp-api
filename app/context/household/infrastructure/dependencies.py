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
    UpdateHouseholdServiceContract,
)
from app.context.household.domain.services import (
    AcceptInviteService,
    CreateHouseholdService,
    DeclineInviteService,
    InviteUserService,
    RemoveMemberService,
    UpdateHouseholdService,
)
from app.context.household.infrastructure.repositories import HouseholdRepository
from app.shared.infrastructure.database import get_db


# Repository dependencies
def get_household_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HouseholdRepositoryContract:
    return HouseholdRepository(db)


# Service dependencies
def get_create_household_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> CreateHouseholdServiceContract:
    return CreateHouseholdService(household_repository)


def get_invite_user_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> InviteUserServiceContract:
    return InviteUserService(household_repository)


def get_accept_invite_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> AcceptInviteServiceContract:
    return AcceptInviteService(household_repository)


def get_decline_invite_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> DeclineInviteServiceContract:
    return DeclineInviteService(household_repository)


def get_remove_member_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> RemoveMemberServiceContract:
    return RemoveMemberService(household_repository)


def get_update_household_service(
    household_repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> UpdateHouseholdServiceContract:
    return UpdateHouseholdService(household_repository)


# Handler dependencies (Commands)
def get_create_household_handler(
    service: Annotated[CreateHouseholdServiceContract, Depends(get_create_household_service)],
) -> CreateHouseholdHandlerContract:
    return CreateHouseholdHandler(service)


def get_invite_user_handler(
    service: Annotated[InviteUserServiceContract, Depends(get_invite_user_service)],
) -> InviteUserHandlerContract:
    return InviteUserHandler(service)


def get_accept_invite_handler(
    service: Annotated[AcceptInviteServiceContract, Depends(get_accept_invite_service)],
) -> AcceptInviteHandlerContract:
    return AcceptInviteHandler(service)


def get_decline_invite_handler(
    service: Annotated[DeclineInviteServiceContract, Depends(get_decline_invite_service)],
) -> DeclineInviteHandlerContract:
    return DeclineInviteHandler(service)


def get_remove_member_handler(
    service: Annotated[RemoveMemberServiceContract, Depends(get_remove_member_service)],
) -> RemoveMemberHandlerContract:
    return RemoveMemberHandler(service)


def get_update_household_handler(
    service: Annotated[UpdateHouseholdServiceContract, Depends(get_update_household_service)],
) -> UpdateHouseholdHandlerContract:
    return UpdateHouseholdHandler(service)


def get_delete_household_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> DeleteHouseholdHandlerContract:
    return DeleteHouseholdHandler(repository)


# Handler dependencies (Queries)
def get_list_household_invites_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> ListHouseholdInvitesHandlerContract:
    return ListHouseholdInvitesHandler(repository)


def get_list_user_pending_invites_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> ListUserPendingInvitesHandlerContract:
    return ListUserPendingInvitesHandler(repository)


def get_get_household_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> GetHouseholdHandlerContract:
    return GetHouseholdHandler(repository)


def get_list_user_households_handler(
    repository: Annotated[HouseholdRepositoryContract, Depends(get_household_repository)],
) -> ListUserHouseholdsHandlerContract:
    return ListUserHouseholdsHandler(repository)
