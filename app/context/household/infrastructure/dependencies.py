from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.household.application.contracts import CreateHouseholdHandlerContract
from app.context.household.application.handlers import CreateHouseholdHandler
from app.context.household.domain.contracts import (
    CreateHouseholdServiceContract,
    HouseholdRepositoryContract,
)
from app.context.household.domain.services import CreateHouseholdService
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


# Handler dependencies
def get_create_household_handler(
    service: CreateHouseholdServiceContract = Depends(get_create_household_service),
) -> CreateHouseholdHandlerContract:
    return CreateHouseholdHandler(service)
